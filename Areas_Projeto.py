class Areas_Projeto():

    def define_papel(argument):
        switcher = {
                "Administrador": "Administrador",
                "Administrador de Dados": "Administrador_Dados",
                "Agente de Compliance": "agente_compliance",
                "Agente de Qualidade": "agente_qualidade",
                "Analista de Segurança": "analista_seguranca",
                "Arquitect Owner": "architect_owner",
                "Dono do Produto (Product Owner - PO)": "dono_produto",
                "Facilitador Ágil": "facilitador_agil",
                "Líder Ágil": "lider_agil",
                "Líder de Negócio": "lider_negocio",
                "Líder de Operação": "lider_operacao",
                "Líder de Solução": "lider_solucao",
                "Líder de TI": "lider_ti",
                "Líder do Time (Squad Leader)": "lider_time",
                "Líder Técnico": "lider_tecnico",
                "Membro do Capítulo": "membro_capitulo",
                "Negócio": "negocio",
                "Suporte da Centralizadora": "suporte_centralizadora",
                "Time (Desenvolvedores)": "time",
                "UX Designer": "ux_designer",
                "Líder de Negócio (Business Owner - BO)": "lider_negocio",
                "Tester": "tester",
                "Líder de Projeto Ágil": "lider_projeto_agil",
                "Analista de Negócio": "analista_negocio",
                "Analista de Métricas": "analistaMetricas"
            }
        return switcher.get(argument, "Papel não encontrado")
