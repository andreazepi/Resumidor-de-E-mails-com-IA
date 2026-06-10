def resumidor_de_emails(lista_de_emails, salvar_em_arquivo=True):
    """
    Função que resume e-mails usando a API do Gemini.
    
    Parâmetros:
    - lista_de_emails: lista com os corpos dos e-mails
    - salvar_em_arquivo: se True, salva os resumos em um arquivo
    """
    
    print("=" * 60)
    print("INICIANDO RESUMIDOR DE E-MAILS")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Total de e-mails a processar: {len(lista_de_emails)}")
    print("=" * 60)
    print()
    
    tempo_inicio = time.time()
    emails_processados = 0
    emails_com_erro = 0
    resumos = []
    
    for numero, email in enumerate(lista_de_emails):
        try:
            print(f"Processando e-mail {numero + 1}/{len(lista_de_emails)}...", end=" ")
            
            resposta = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=f"""Vou te mandar o corpo de um e-mail. Quero que você o resuma em apenas 1 linha,
passando o intuito daquele e-mail. Segue o e-mail: {email}"""
            )
            
            resumo = resposta.text
            resumos.append(f"E-mail {numero + 1}: {resumo}")
            
            print("✓ Concluído")
            print(f"E-mail {numero + 1}: {resumo}")
            print("-" * 60)
            
            emails_processados += 1
            
            # Aguarda 1 segundo entre requisições para evitar quota
            time.sleep(1)
            
        except Exception as erro:
            emails_com_erro += 1
            mensagem_erro = f"E-mail {numero + 1}: ERRO - {str(erro)}"
            resumos.append(mensagem_erro)
            print(f"✗ Erro: {str(erro)[:50]}...")
            print(mensagem_erro)
            print("-" * 60)
    
    # Calcula tempo total
    tempo_total = time.time() - tempo_inicio
    
    # Salva em arquivo se solicitado
    if salvar_em_arquivo:
        nome_arquivo = f"resumos_emails_{datetime.now().strftime('%d%m%Y_%H%M%S')}.txt"
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
                arquivo.write("RESUMO DE E-MAILS\n")
                arquivo.write(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                arquivo.write("=" * 60 + "\n\n")
                for resumo in resumos:
                    arquivo.write(resumo + "\n")
            print(f"\n✓ Arquivo salvo: {nome_arquivo}")
        except Exception as erro:
            print(f"\n✗ Erro ao salvar arquivo: {str(erro)}")
    
    # Exibe estatísticas
    print("\n" + "=" * 60)
    print("ESTATÍSTICAS FINAIS")
    print("=" * 60)
    print(f"Total de e-mails processados: {emails_processados}")
    print(f"Total de erros: {emails_com_erro}")
    print(f"Taxa de sucesso: {(emails_processados / len(lista_de_emails) * 100):.1f}%")
    print(f"Tempo total: {tempo_total:.2f} segundos")
    print(f"Tempo médio por e-mail: {(tempo_total / len(lista_de_emails)):.2f} segundos")
    print("=" * 60)
