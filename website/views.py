from django.shortcuts import render, redirect 
from django.core.mail import send_mail 
from django.conf import settings 
from .models import Project, Service, GalleryImage

def home(request):
    return render(request, 'home.html', {}) 

def about(request):
    context = {
        'company_name': 'JURIDIO CHICALA CONSTRUÇÕES, E.I.',
        'year_established': 2020 
    }
    return render(request, 'about.html', context)

def portfolio(request):
    # CORREÇÃO: Usa 'date_completed' em vez de 'completion_date'
    projects = Project.objects.all().order_by('-date_completed')
    
    context = {
        'page_title': 'O Nosso Portfólio de Construção',
        'projects': projects
    }
    return render(request, 'portfolio.html', context)

def services(request):
    context = {
        'page_title': 'Nossos Serviços de Engenharia e Construção',
        'service_list': [
            {'title': 'Construção Civil', 'description': 'Edifícios residenciais, comerciais e infraestruturas públicas.'},
            {'title': 'Reforma e Remodelação', 'description': 'Renovação de interiores e exteriores, e modernização de espaços existentes.'},
            {'title': 'Obras Elétricas e Hidráulicas', 'description': 'Instalação e manutenção de sistemas elétricos e canalizações.'},
            {'title': 'Gestão de Projetos', 'description': 'Planeamento, supervisão e controlo de todo o ciclo de vida da obra.'},
        ]
    }
    return render(request, 'services.html', context)

def contact(request):
    context = {
        'phone': getattr(settings, 'COMPANY_PHONE', '+258 XXXXXXXX'),
        'email': getattr(settings, 'COMPANY_EMAIL', 'contacto@jcc.co.mz'),
        'address': getattr(settings, 'COMPANY_ADDRESS', 'Morada Não Definida'),
        'social_media': {
            'facebook': getattr(settings, 'SOCIAL_FACEBOOK', '#'),
            'linkedin': getattr(settings, 'SOCIAL_LINKEDIN', '#'),
        },
        'success_message': None,
        'error_message': None,
        'form_data': {}
    }
    
    if request.method == 'POST':
        name = request.POST.get('name')
        sender_email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        full_message = f"Nome: {name}\nEmail: {sender_email}\n\nAssunto: {subject}\n\nMensagem:\n{message}"
        
        try:
            send_mail(
                subject=f"NOVO CONTACTO: {subject}", 
                message=full_message, 
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@jcc.co.mz'), 
                recipient_list=[context['email']], 
                fail_silently=False,
            )
            
            return redirect('success_page') 
            
        except Exception:
            context['error_message'] = 'Ocorreu um erro ao enviar a mensagem. Por favor, tente novamente mais tarde.'
            context['form_data'] = {'name': name, 'email': sender_email, 'subject': subject, 'message': message}
            
    return render(request, 'contact.html', context)

def quote_request(request):
    if request.method == 'POST':
        name = request.POST.get('nome')  
        email = request.POST.get('email')  
        phone = request.POST.get('telefone') 
        company = request.POST.get('empresa') 
        
        service_type = request.POST.get('servico') 
        location = request.POST.get('localizacao') 
        area = request.POST.get('area')
        deadline = request.POST.get('prazo')
        description = request.POST.get('descricao')
        
        uploaded_files = request.FILES.getlist('ficheiros')
        attachments = []
        for file in uploaded_files:
            attachments.append((file.name, file.read(), file.content_type))

        email_body = f"""
--- NOVO PEDIDO DE ORÇAMENTO (JCC CONSTRUÇÕES) ---
--------------------------------------------------
Nome: {name}
Email: {email}
Telefone: {phone}
Serviço: {service_type}
Localização: {location}
Área (m²): {area}
Prazo Desejado: {deadline}
Empresa: {company if company else 'N/A'}

DESCRIÇÃO:
{description}
"""

        try:
            send_mail(
                subject=f'NOVO ORÇAMENTO: {service_type} - De: {name}', 
                message=email_body, 
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@jcc.co.mz'), 
                recipient_list=[getattr(settings, 'COMPANY_EMAIL', 'contacto@jcc.co.mz')], 
                fail_silently=False,
                attachments=attachments 
            )
        except Exception as e:
            print(f"ERRO CRÍTICO no envio de email de orçamento: {e}") 

        return redirect('success_page') 

    return redirect('services') 

def success_page(request):
    context = {
        'title': 'Pedido Enviado com Sucesso',
        'message_line1': 'Obrigado pelo seu contacto!',
        'message_line2': 'A nossa equipa entrará em contacto em breve.'
    }
    return render(request, 'success.html', context)

def gallery(request):
    image_list = GalleryImage.objects.all()
    context = {
        'page_title': 'Galeria de Obras e Equipamentos',
        'image_list': image_list
    }
    return render(request, 'gallery.html', context)