Leilão
======

Leilão é um loja virtual feita com Django que tem por objetivo possibilitar as
pessoas de vender seus pertences sem intermediários e taxas extras. É informal,
simples e objetivo.

Requisitos
----------

- Django 1.3

Instalação
==========

Instalar o Leilão é bem fácil, uma vez satisfeitos os requisitos.

Clone o repositório, crie o banco de dados e inicie o servidor:

    git clone git://github.com/cabello/leilao.git
    cd leilao
    python manage.py syncdb
    python manage.py runserver

Feito isso, você terá disponível a loja em http://localhost:8000 e a seção
administrativa fica em http://localhost:8000/admin, você já pode navegar pelo
site e adicionar seus produtos.

Licença
=======

O projeto Leilão segue a licença BSD igual ao Django.