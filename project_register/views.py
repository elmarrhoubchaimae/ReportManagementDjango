from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm, PDFUploadForm, SearchStudentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Profile, PDFUpload
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import PyPDF2
from transformers import BertTokenizer, BertModel
import string

# Define the keywords
problem_keywords = [
    "problem", "issue", "challenge", "problématique", "objectif", "difficulty", 
    "obstacle", "concern", "limitation", "constraint", "drawback", "complication", 
    "risk", "bottleneck", "hurdle", "dilemma", "crisis", "trouble", "pain point",
    "Notre problématique est la suivante",
    "La problématique que nous abordons est la suivante",
    "Voici la problématique sur laquelle nous nous penchons",
    "Notre question centrale est la suivante",
    "La question que nous cherchons à résoudre est la suivante",
    "La problématique principale de notre étude est la suivante",
    "Nous nous concentrons sur la problématique suivante",
    "La problématique que nous avons identifiée est la suivante",
    "Voici la problématique que nous avons définie",
    "La problématique que nous allons traiter est la suivante",
    "Notre analyse porte sur la problématique suivante",
    "Le sujet que nous allons traiter est le suivant",
    "La question soulevée dans cette étude est la suivante",
    "La problématique de cette recherche est la suivante",
    "Notre travail se concentre sur la problématique suivante",
    "La problématique que nous souhaitons explorer est la suivante",
    "Le problème central de cette étude est le suivant",
    "La question principale que nous examinons est la suivante",
    "La problématique étudiée est la suivante",
    "Nous nous interrogeons sur la problématique suivante",
    "Notre enquête porte sur la problématique suivante",
    "Le défi que nous abordons est le suivant",
    "La problématique que nous analysons est la suivante",
    "L'enjeu principal de notre étude est le suivant",
    "La problématique que nous avons choisi d'explorer est la suivante"
]

solution_keywords = [
    "solution", "approach", "méthode", "proposed", "propose", "solution proposée", 
    "aims", "aimed", "aiming", "solve", "resolve", "fix", "remedy", 
    "overcome", "strategy", "plan", "implementation", "action", "intervention", 
    "treatment", "measure", "tactic", "improvement", "innovation", "optimization", 
    "enhancement", "resolution",
    "La solution trouvée pour ce problème est :",
    "La solution que nous proposons est la suivante :",
    "La solution retenue pour résoudre ce problème est :",
    "Voici la solution apportée à ce problème :",
    "La solution mise en œuvre est la suivante :",
    "La réponse à ce problème est la suivante :",
    "La solution que nous avons identifiée est :",
    "La solution à ce défi est :",
    "La solution adoptée pour ce problème est :",
    "La résolution de ce problème passe par :",
    "La solution recommandée est la suivante :",
    "La solution apportée est :",
    "Notre réponse à ce problème est :",
    "La solution suggérée pour ce problème est :",
    "La solution envisagée est la suivante :",
    "La solution que nous avons développée est :",
    "La solution idéale pour ce problème est :",
    "La solution que nous avons mise en place est :",
    "La solution optimale pour ce problème est :",
    "La solution que nous avons trouvée est :",
    "La solution que nous proposons consiste en :",
    "La réponse que nous avons apportée à ce problème est :",
    "Voici la solution que nous avons mise au point :",
    "La solution adoptée dans ce contexte est :",
    "La solution formulée pour ce problème est :"
]

tools_keywords = [
    # Langages de programmation
    "C", "C++", "Java", "Python", "JavaScript", "Ruby", "PHP", "Swift", "Kotlin", "Rust", "Go", "Dart",
    "TypeScript", "C#", "Perl", "R", "MATLAB", "Scala", "Haskell", "Objective-C", "Visual Basic",
    "Assembly", "Fortran", "COBOL", "Lisp", "Scheme", "F#", "Elixir", "Erlang", "Groovy", "Smalltalk",
    "Julia", "VHDL", "Verilog", "Ada", "Lua", "Solidity", "PL/SQL", "Shell", "Bash", "PowerShell",
    "Tcl", "Prolog", "AWK", "SAS", "Simula", "ML", "Racket", "OCaml", "D", "Nim", "Crystal", "Eiffel",
    "ActionScript", "Forth", "PureBasic", "Pascal", "Delphi", "Clipper", "FoxPro", "REXX", "APL",
    
    # Frameworks et bibliothèques backend
    "Django", "Flask", "Express.js", "Spring Boot", "Ruby on Rails", "Laravel", "ASP.NET", "FastAPI",
    "NestJS", "Koa", "Play Framework", "Gin", "Phoenix", "Sinatra", "CakePHP", "Symfony", "Sails.js",
    "Pyramid", "Tornado", "Bottle", "Coldfusion", "Ionic", "Next.js", "Nuxt.js", "Meteor", "Blazor",
    "Struts", "Blade", "Vaadin", "Tapestry", "JHipster", "Fiber", "Goa", "Echo",

    # Frameworks et bibliothèques frontend
    "ReactJs","NodeJs", "Angular", "Vue.js", "Svelte", "Ember.js", "Backbone.js", "jQuery", "Bootstrap",
    "Foundation", "Material-UI", "Semantic UI", "Tailwind CSS", "Bulma", "Chakra UI", "Lit", "Alpine.js",
    "Stencil", "Riot.js", "Preact", "Inferno", "Mithril", "Aurelia", "Gatsby", "Sapper",

    # Outils de versionnage
    "Git", "Subversion (SVN)", "Mercurial", "CVS", "Perforce", "Bazaar", "ClearCase", "TFS", "Bitbucket",
    "GitHub", "GitLab", "Azure DevOps", "SourceForge", "Fossil", "Monotone", "Plastic SCM",

    # IDEs et éditeurs de texte
    "Visual Studio Code", "IntelliJ IDEA", "Eclipse", "PyCharm", "WebStorm", "NetBeans", "Android Studio",
    "Xcode", "Atom", "Sublime Text", "Notepad++", "Brackets", "Vim", "Emacs", "Visual Studio", "Komodo Edit",
    "Geany", "BlueJ", "IDLE", "Code::Blocks", "KDevelop", "JDeveloper", "RStudio", "Aptana Studio",
    "Codelite", "SlickEdit", "Wing IDE", "Anjuta", "Monodevelop", "PHPStorm",

    # Outils de gestion de projet
    "Jira", "Asana", "Trello", "Monday.com", "Redmine", "ClickUp", "Wrike", "Basecamp", "Notion",
    "Microsoft Project", "Taiga", "KanbanFlow", "Linear", "Clubhouse", "YouTrack", "Zoho Projects",
    "GanttProject",

    # Outils CI/CD
    "Jenkins", "Travis CI", "CircleCI", "GitHub Actions", "GitLab CI/CD", "Bamboo", "TeamCity",
    "Azure Pipelines", "Drone", "Buddy", "Spinnaker", "CodeShip", "ArgoCD", "Tekton", "Flux",
    "GoCD", "Concourse", "Semaphore", "Octopus Deploy", "Bitrise",

    # Outils de conteneurisation et d'orchestration
    "Docker", "Kubernetes", "OpenShift", "Rancher", "Amazon ECS", "Podman", "Nomad", "Docker Swarm",
    "Mesos", "Containerd", "LXC/LXD", "Fargate", "MicroK8s", "EKS", "GKE", "AKS", "Helm",

    # Bases de données
    "MySQL", "PostgreSQL", "SQLite", "MongoDB", "Redis", "Oracle Database", "Microsoft SQL Server",
    "MariaDB", "Cassandra", "CouchDB", "DynamoDB", "Neo4j", "Elasticsearch", "Firebase", "Memcached",
    "Couchbase", "HBase", "Bigtable", "RavenDB", "OrientDB", "ArangoDB", "Riak", "VoltDB", "InfluxDB",
    "LevelDB", "TimescaleDB", "ClickHouse", "Aerospike", "Merise", "UML", "NoSQL", "PL/SQL", "jira", "SQL server"

    # Outils de tests
    "JUnit", "Selenium", "PyTest", "Mocha", "Jest", "RSpec", "Cypress", "Postman", "TestNG",
    "Appium", "Robot Framework", "xUnit", "QUnit", "Jasmine", "Protractor", "Karma", "Mockito",
    "Cucumber", "Chai", "NUnit", "SpecFlow", "Geb", "Gatling", "SoapUI", "LoadRunner", "JMeter",

    # Outils de virtualisation et de cloud computing
    "AWS", "Microsoft Azure", "Google Cloud", "IBM Cloud", "DigitalOcean", "Vagrant", "VMware",
    "VirtualBox", "Hyper-V", "KVM", "Proxmox", "Parallels Desktop", "QEMU", "OpenStack",
    "Linode", "Heroku", "Oracle Cloud", "Cloud Foundry", "Alibaba Cloud",

    # Systèmes d'exploitation
    "Windows", "Linux", "MacOS", "Ubuntu", "CentOS", "Debian", "Fedora", "Arch Linux", "Red Hat",
    "FreeBSD", "Solaris", "Kali Linux", "OpenSUSE", "Alpine Linux", "Android", "iOS", "Haiku",
    "ReactOS", "Chromium OS", "Chrome OS", "Slackware", "Gentoo", "Mandriva", "Mint", "Tails",

    # Outils de monitoring
    "Prometheus", "Grafana", "Nagios", "Zabbix", "Datadog", "New Relic", "Splunk", "Elastic Stack",
    "Dynatrace", "AppDynamics", "CloudWatch", "Pingdom", "SolarWinds", "Sensu", "Cacti", "Icinga",

    # Outils DevOps et automation
    "Ansible", "Chef", "Puppet", "Terraform", "SaltStack", "Vagrant", "Packer", "Consul", "Vault",
    "Elastic Beanstalk", "CodeDeploy", "Lambda", "Serverless Framework", "CFEngine", "Nomad",

    # Outils de gestion de paquets
    "npm", "Yarn", "pip", "Composer", "NuGet", "Gradle", "Maven", "Cargo", "Bundler", "Homebrew",
    "Apt", "Dnf", "Pacman", "Chocolatey", "Conda", "Gems", "Bower", "Hex", "Spack",

    # Langages de script et shell
    "Bash", "Zsh", "Fish", "Powershell", "KornShell", "Tcsh", "Csh", "Python", "Perl", "Ruby",
    "Lua", "Groovy", "VBScript", "AutoHotkey", "AWK", "Sed", "Rexx", "JScript",

    # Outils de documentation
    "Swagger", "Postman", "Sphinx", "MkDocs", "JSDoc", "Doxygen", "Slate", "Jekyll", "Hugo",
    "GitBook", "Confluence", "Notion", "ReadTheDocs", "Asciidoctor", "Redoc", "Antora",

    # Outils de collaboration et de communication
    "Slack", "Microsoft Teams", "Discord", "Zoom", "Google Meet", "Skype", "Mattermost", "Rocket.Chat",
    "Trello", "Miro", "Figma", "Mural", "Workplace", "Chanty", "Webex", "Zoho Cliq",

    # Outils d'analyse de code
    "SonarQube", "ESLint", "Prettier", "Pylint", "Stylelint", "Checkstyle", "FindBugs", "PMD",
    "Cppcheck", "Bandit", "Brakeman", "Rubocop", "JSHint", "PHPCS", "Detekt", "Coverity",
    "Codacy", "CodeClimate", "Snyk", "Semgrep", "Fossa"

]

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def extract_cover_page_info(text):
    name_student = ""
    field = ""
    abstract = ""
    enc_interne = ""
    enc_externe = ""
    contact_interne = ""
    contact_externe = ""
    entreprise = ""

    lines = text.split('\n')

    for line_idx, line in enumerate(lines):
        if any(phrase in line.lower() for phrase in ["présenté par :", "soutenu par :", "réalisé par :"]):
            if len(lines) > line_idx + 1:
                name_student = lines[line_idx + 1].strip()

        if "Filière " in line:
            if line.strip().startswith("Filière "):
                field = line.split("Filière ")[1].strip()
            elif len(lines) > line_idx + 1:
                field = lines[line_idx + 1].strip()

        if "en partenariat avec" in line.lower():
            entreprise_parts = line.split("en partenariat avec")
            if len(entreprise_parts) > 1:
                entreprise = entreprise_parts[1].strip()
            elif len(lines) > line_idx + 1:
                entreprise = lines[line_idx + 1].strip()
            else:
                entreprise = line.split("en partenariat avec")[1].strip()
        if "enc_interne:" in line.lower():
            if line_idx + 1 < len(lines):
                enc_interne = lines[line_idx ].strip()

        if "enc_interne:" in line.lower():
            if line_idx + 1 < len(lines):
                contact_interne = lines[line_idx +1 ].strip()

        if "enc_externe:" in line.lower():
            if line_idx + 1 < len(lines):
                enc_externe = lines[line_idx ].strip()

        if "enc_externe:" in line.lower():
            if line_idx + 1 < len(lines):
                contact_externe = lines[line_idx +1 ].strip()
    
    abstract_start_idx = 0

    for line_idx, line in enumerate(lines):
        if "Résumé" in line.lower():
            abstract_start_idx = line_idx
            break

    abstract_lines = []
    for line_idx in range(abstract_start_idx + 1, len(lines)):
        line = lines[line_idx].strip()
        if line.lower().startswith("keywords") or line.lower().startswith("mots-clés"):
            break
        abstract_lines.append(line)

    abstract = "\n".join(abstract_lines)

    return name_student, field, abstract, enc_interne, enc_externe, contact_interne, contact_externe, entreprise

def extract_info_from_abstract(abstract):
    sentences = abstract.split('.')
    problem_text = []
    solution_text = []
    tools_text = []
    role_enc_interne_text = []
    role_enc_externe_text = []

    for sentence in sentences:
        sentence_tokens = tokenizer.tokenize(sentence.lower())
        problem_part = extract_after_keyword(sentence, problem_keywords)
        solution_part = extract_after_keyword(sentence, solution_keywords)
        tools_part = extract_tools_from_sentence(sentence, tools_keywords)  # Remplacement par extract_tools_from_sentence
        role_enc_interne = extract_after_keyword(sentence, ["encadrant interne", "encadrante interne", "tuteur interne", "tutrice interne"])
        role_enc_externe = extract_after_keyword(sentence, ["encadrant externe", "encadrante externe", "tuteur externe", "tutrice externe"])

        if problem_part:
            problem_text.append(problem_part)
        if solution_part:
            solution_text.append(solution_part)
        if tools_part:
            tools_text.append(tools_part)
        if role_enc_interne:
            role_enc_interne_text.append(role_enc_interne)
        if role_enc_externe:
            role_enc_externe_text.append(role_enc_externe)

    # Pour les outils, séparer par des virgules et ajouter un point à la fin
    formatted_tools_text = ", ".join(tools_text) + "." if tools_text else ""

    return " ".join(problem_text), " ".join(solution_text), formatted_tools_text, " ".join(role_enc_interne_text), " ".join(role_enc_externe_text)

def extract_after_keyword(sentence, keywords):
    for keyword in keywords:
        if keyword in sentence.lower():
            keyword_idx = sentence.lower().index(keyword)
            return sentence[keyword_idx + len(keyword):].strip()
    return None

def extract_tools_from_sentence(sentence, tools_keywords):
    """Extraire les outils mentionnés dans une phrase donnée en ignorant la ponctuation."""
    # Supprimer la ponctuation et convertir la phrase en minuscules
    translator = str.maketrans('', '', string.punctuation)
    cleaned_sentence = sentence.translate(translator).lower()
    
    # Diviser la phrase en mots
    words = cleaned_sentence.split()
    
    # Utiliser un ensemble pour éviter les doublons
    tools_found = set(tool for tool in tools_keywords if tool.lower() in words)
    
    # Retourner les outils trouvés sous forme de chaîne, ou None si aucun outil n'est trouvé
    return ", ".join(tools_found) if tools_found else None
@csrf_protect
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'profile'):
                if user.profile.user_type == 'student':
                    return redirect('/student_page/')
                elif user.profile.user_type == 'professor':
                    return redirect('/professor_page/')
            return redirect('/home/')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})
    
def update_status(request, pdf_id):
    if request.method == 'POST':
        pdf = get_object_or_404(PDFUpload, id=pdf_id)
        if request.user.profile.user_type == 'professor':  # Ensure only professors can update
            new_status = request.POST.get('status')
            pdf.status = new_status
            pdf.save()
            return redirect('search_student')

@login_required
def upload_pdf(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.error(request, "Profile does not exist.")
        return redirect('home')

    if profile.user_type != 'student':
        messages.error(request, "Only students can upload PDFs.")
        return redirect('home')

    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_upload = form.save(commit=False)
            pdf_upload.user = request.user
            pdf_upload.save()
            messages.success(request, "PDF uploaded successfully!")
            return redirect('upload_pdf')  # or redirect to any other page you want
    else:
        form = PDFUploadForm()

    pdfs = PDFUpload.objects.filter(user=request.user)
    return render(request, 'authenticate/upload_pdf.html', {'form': form, 'pdfs': pdfs})

@login_required
def delete_pdf(request, pdf_id):
    pdf = get_object_or_404(PDFUpload, id=pdf_id, user=request.user)
    if request.method == 'POST':
        pdf.delete()
        messages.success(request, "PDF deleted successfully!")
        return redirect('home')
    return redirect('home')

@login_required
def search_student(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            student = User.objects.get(username=username)
            pdfs = PDFUpload.objects.filter(user=student)
            return render(request, 'authenticate/search_student.html', {'student': student, 'pdfs': pdfs})
        except User.DoesNotExist:
            messages.error(request, "Student does not exist.")
            return redirect('search_student')
    return render(request, 'authenticate/search_student.html')

def search_by_sujet(request):
    query = request.GET.get('sujet')
    results = []
    
    if query:
        results = PDFUpload.objects.filter(sujet__icontains=query)  # Case-insensitive search

    return render(request, 'authenticate/search_page.html', {'results': results, 'query': query})

@csrf_protect
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal

            profile = user.profile
            profile.user_type = form.cleaned_data.get('user_type')
            if profile.user_type == 'student':
                profile.school_year = form.cleaned_data.get('school_year')
                profile.field = form.cleaned_data.get('field')
            elif profile.user_type == 'professor':
                profile.department = form.cleaned_data.get('department')

            profile.save()  # Save the updated profile

            login(request, user)
            messages.success(request, "Registration successful! Welcome, {}.".format(user.username))
            return redirect('/home/')
        else:
            messages.error(request, "There was an error with your registration. Please try again.")
    else:
        form = RegisterUserForm()
    return render(request, 'authenticate/register.html', {'form': form})

@login_required
def home(request):
    user = request.user
    context = {}

    if user.profile.user_type == 'student':
        if request.method == 'POST':
            form = PDFUploadForm(request.POST, request.FILES)
            if form.is_valid():
                pdf_upload = form.save(commit=False)
                pdf_upload.user = request.user
                pdf_upload.save()
                messages.success(request, "PDF uploaded successfully!")
                return redirect('home')
        else:
            form = PDFUploadForm()

        pdfs = PDFUpload.objects.filter(user=user)
        context.update({
            'form': form,
            'pdfs': pdfs,
        })

    elif user.profile.user_type == 'professor':
        student = None
        pdfs = None
        summary = None

        if request.method == 'POST':
            if 'username' in request.POST:
                form = SearchStudentForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data.get('username')
                    try:
                        student = User.objects.get(username=username)
                        pdfs = PDFUpload.objects.filter(user=student)
                    except User.DoesNotExist:
                        student = None
            elif 'summarize_pdf_id' in request.POST:
                pdf_id = request.POST.get('summarize_pdf_id')
                pdf = get_object_or_404(PDFUpload, id=pdf_id)
                text = extract_text_from_pdf(pdf.file.path)
                name_student, field, abstract, enc_interne, enc_externe, contact_interne, contact_externe, entreprise = extract_cover_page_info(text)
                problem_text, solution_text, tools_text,role_enc_interne_text, role_enc_externe_text = extract_info_from_abstract(abstract)
                summary = {
                    "name_student": name_student,
                    "field": field,
                    "problem_text": problem_text,
                    "solution_text": solution_text,
                    "tools_text": tools_text,
                    "enc_interne": enc_interne,
                    "enc_externe": enc_externe,
                    "contact_interne": contact_interne,
                    "contact_externe": contact_externe,
                    "entreprise": entreprise,
                }

        form = SearchStudentForm()
        context.update({
            'form': form,
            'student': student,
            'pdfs': pdfs,
            'summary': summary,
        })

    return render(request, 'authenticate/home.html', context)

def welcome(request):
    return render(request, 'authenticate/welcome.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out!")
    return redirect('login')

@login_required
def student_page(request):
    return render(request, 'authenticate/upload_pdf.html')

@login_required
def professor_page(request):
    return render(request, 'authenticate/search_student.html')

def student(request):
    user = request.user
    context = {}

    # Ensure the user is a student
    if user.profile.user_type == 'student':
        
        # Handling POST request (uploading the PDF)
        if request.method == 'POST':
            form = PDFUploadForm(request.POST, request.FILES)
            if form.is_valid():
                pdf_upload = form.save(commit=False)
                pdf_upload.user = request.user  # Associate PDF with the current student user
                pdf_upload.save()
                messages.success(request, "PDF uploaded successfully!")
                return redirect('home')  # Ensure this URL exists
        else:
            form = PDFUploadForm()

        # Fetching PDFs uploaded by the current user (student)
        pdfs = PDFUpload.objects.filter(user=user)
        
        # Update context with form and PDFs
        context.update({
            'form': form,
            'pdfs': pdfs,
        })

        # Render the student's page with form and uploaded PDFs
        return render(request, 'authenticate/student.html', context)
    
    else:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
