#Na raiz do projeto, a primeira vez execute
#chmod +x start.sh
#No terminal para tornar esse script executável

#Depois, basta o comando ./start.sh para iniciar a variavel de ambiente e rodar a aplicação

source venv/bin/activate
uvicorn main:app --reload