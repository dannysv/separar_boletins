0) Requisitos
	a) Para executar os scripts python é necessario ter instalado o textract
	b) Para compilar e executar os scripts java é necessario baixar a livraria
		pdfbox-app-2.0.1.jar

1) Organizar os dados(Boletins)
	a) Os boletins são organizados em 3 pastas(Boletins1, Boletins2, Boletins3), só pelo ordem de disponibilização dos mesmos
	b) E uma pasta adicional onde são agrupados aqueles pdf's que precisam ser processados usando OCR
	c) no total são 215 boletins
	
	d) para criar a estrutura de pastas, executar seguinte comando
		python criar.py
	
	e) Os pdfs(boletins) devem ser copiados nas pastas "Boletins1, Boletins2, Boletins3, Boletins4"
			separar_boletins/
				data/
					Boletins/
						Boletins1/
						Boletins2/
						Boletins3/
						Boletins4/
	f) A livraria deve ser copiada na pasta 
			separar_boletins/
				jar/

2) Editar os textos(com pdfbox)
	- Como entrada recebe os pastas que contem os boletins
	- Adicionar uma página com um label, no caso com o texto "### new line ###"
		- requisitos
			adicionar a livraria java(pdfbox) na pasta "jar" 
		- comando
			javac -cp ../jar/pdfbox-app-2.0.1.jar:. edit_pdf.java(compilar)
			java -cp ../jar/pdfbox-app-2.0.1.jar:. edit_pdf(executar)
		- observação :  está etapa poderia ser evitada, se é posivel encontrar um jeito de saber onde acaba cada pagina no boletim, ou saber o número de páginas, mas depende da ferramenta que é usada.
	- como saida retorna os boletins editados com páginas adicionais como labels

3) Recuperar os indices onde começa cada artigo dentro dos boletins
	a) como entrada recebe os pastas que contem os boletins editados da etapa anterior
	b) Extrair o texto dos pdfs e adicionar o número de pagina em cada linha de texto
		- observação: Em esta parte, se não foi possível extrair o texto com os extratores(tika, pdfbox, etc), passamos a usar o OCR(na implementação, só usamos o OCR que vem no textract)
	c) Salvar os textos extraidos numerados
	d) Procurar por palavras chave(por exemplo : "RESUMO", "resumo", etc.) e extrair o número de pagina correspondente como o começo de um artigo
		- requisitos
			instalar textract(está parte pode ser substituida com qualquer outro extrator)
		- comando
			python get_indicespapers.py
		- observação: procurar por palavras chave ou guia, acabariam sendo simples heuristicas, que podem ser incrementadas ou melhoradas, vendo as caracteristicas dos documentos processados(boletins)
	e) retornar como saida e por cada boletim, os indices de começo de cada artigo(*)

4) Dividir os boletins a partir da saida da etapa anterior
	a) como entrada recebe os pastas que contem os boletins e os indices criados na etapa anterior
	b) separar os boletins levando em consideração os indices recuperados na etapa anterior
		- requisitos
			adicionar a livraria java(pdfbox) no pasta "jars" 
		- comando
			- javac -cp ../jar/pdfbox-app-2.0.1.jar:. get_papers.java
			- java -cp ../jar/pdfbox-app-2.0.1.jar:. get_papers
	c) retornar como saida e por cada boletim, os artigos que são encontrados

5) Extrair textos dos artigos encontrados 
	a) comando
		- python textract_pdfminer.py
	b) retornar como saida e por cada boletim os textos por cada artigo

6) Resultados
	- 200 dos 215 boletins foram divididos corretamente, dentro de estes estão também os que foram processados com OCR
	- Dos 15 que não foi possível separar por artigos, a maioria tem o problema na etapa de extração, mesmo usando o OCR do textract o resultado são arquivos vazios ou com texto sem o formato requerido.

7) Repositorio
	Finalmente, o repositorio é disponibilazado em:
		- 
	Para poder executar os scripts do repositorio seguir os passos:
	a) git clone link
	c) copiar os pdfs(boletins) nas pastas e a livraria java conforme é descrito na parte "1.e" e "1.f" 
	d) entrar na pasta code/ e executar os seguintes comandos
		- python criar.py
		- javac -cp ../jar/pdfbox-app-2.0.1.jar:. edit_pdf.java(compilar)
 		- java -cp ../jar/pdfbox-app-2.0.1.jar:. edit_pdf(executar)
		- javac -cp ../jar/pdfbox-app-2.0.1.jar:. get_papers.java
 		- java -cp ../jar/pdfbox-app-2.0.1.jar:. get_papers
		- python textract_pdfminer.py

