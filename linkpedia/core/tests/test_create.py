from django.test import TestCase
from core.models import LinkModel
from django.urls import reverse
from django.contrib.auth.models import User

class LinkTest(TestCase):
    
    def test_requires_login(self):

        response = self.client.get(
            reverse('create')
        )

        # Retornando 302 (redirect) caso o usuário não esteja autenticado
        self.assertEqual(response.status_code, 302)

    def test_create(self):
        # Criando autenticação temporária para o teste depois de fechar a rota para usuários autenticados
        user = User.objects.create_user(
            username='aluno',
            password='fatec'
        )
        # Logando com o acesso temporário
        self.client.login(
            username='aluno',
            password='fatec'
        )
        # Executando o create baseado no model
        response = self.client.post(
            reverse('create'), {
                'titulo': 'Google',
                'link': 'https://www.google.com',
                'observacao': 'Buscador oficial do google'
            }
        )
        # Verificando se o status 302 (redirect) é enviado no final do método
        self.assertEqual(response.status_code, 302)
        # Verificando se o objeto é instanciado no banco
        self.assertEqual(
            LinkModel.objects.count(), 1
        )

        link = LinkModel.objects.first()

        self.assertEqual(link.titulo, 'Google')

    def test_create_invalid_link(self):
        # Criando autenticação temporária no banco
        user = User.objects.create_user(
            username='aluno',
            password='fatec'
        )

        # Logando temporariamente para o teste
        self.client.login(
            username='aluno',
            password='fatec'
        )

        # Criando um falso objeto vazio
        response = self.client.post(
            reverse('create'),
            {
                'titulo': '',
                'link': ''
            }
        )

        # Verificando a resposta HTTP
        self.assertEqual(response.status_code, 200)

        # Certificando que o objeto não foi criado no banco
        self.assertEqual(LinkModel.objects.count(), 0)

        self.assertContains(response, 'O título é obrigatório')

    def test_template(self):
        # Criando usuário temporário para autenticação
        user = User.objects.create_user(
            username='aluno',
            password='fatec'
        )

        self.client.login(
            username='aluno',
            password='fatec'
        )

        response = self.client.post(
            reverse('create')
        )

        self.assertTemplateUsed(
            response, 'create.html'
        )