from django.test import TestCase
from core.models import LinkModel
from django.urls import reverse
from django.contrib.auth.models import User

class LinkTest(TestCase):

    def test_requires_login(self):

        link = LinkModel.objects.create(
            titulo="Google",
            link="https://www.google.com"
        )
        
        response = self.client.get(
            reverse('edit', args=[link.id])
        )

        self.assertEqual(response.status_code, 302)

    def test_update_authenticated(self):
        # Criando login temporário
        user = User.objects.create_user(
            username='aluno',
            password='fatec'
        )
        # Logando temporáriamente
        self.client.login(
            username='aluno',
            password='fatec'   
        )

        # Instanciando um objeto no banco
        link = LinkModel.objects.create(
            titulo = 'Google',
            link='https://www.google.com'
        )
        
        # Criando uma rota temporária
        response = self.client.get(
            reverse('edit', args=[link.id])
        )

        # Testando a resposta
        self.assertEqual(response.status_code, 200)

    def test_update_noexist_link(self):
        # Criando um usuário temporário
        user = User.objects.create_user(
            username='aluno',
            password='fatec'
        )
        # Logando o usuário temporariamente
        self.client.login(
            username='aluno',
            password='fatec'
        )

        # Criando a rota temporária e passando um ID inexistente como parâmetro
        response = self.client.get(
            reverse('edit', args=[999])
        )

        # Testando a resposta
        self.assertEqual(response.status_code, 404)