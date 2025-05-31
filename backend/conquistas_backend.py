from .conexao import conectar

def atualizar_conquistas(conquistas):
    """
    Atualiza a quantidade de livros de cada conquista.
    Se não existir, insere uma nova.
    
    Args:
        conquistas: Lista de dicionários {'nome': str, 'quantidade': int}
    
    Returns:
        tuple: (sucesso: bool, mensagem: str)
    """
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        for conquista in conquistas:
            # Tenta atualizar a conquista existente
            cursor.execute("""
                UPDATE Conquistas
                SET QuantidadeLivros = ?
                WHERE Nome = ?
            """, (conquista['quantidade'], conquista['nome']))
            
            # Se não atualizou nenhuma linha, insere nova conquista
            if cursor.rowcount == 0:
                cursor.execute("""
                    INSERT INTO Conquistas (Nome, QuantidadeLivros)
                    VALUES (?, ?)
                """, (conquista['nome'], conquista['quantidade']))
        
        conn.commit()
        return True, "Conquistas atualizadas com sucesso!"
    
    except Exception as e:
        if conn:
            conn.rollback()
        return False, f"Erro ao atualizar conquistas: {str(e)}"
    
    finally:
        if conn:
            conn.close()


def obter_conquistas():
    """
    Obtém todas as conquistas do banco de dados.
    
    Returns:
        list: Lista de dicionários {'id': int, 'nome': str, 'quantidade': int}
    """
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT IdConquista, Nome, QuantidadeLivros FROM Conquistas")
        
        conquistas = [
            {'id': row[0], 'nome': row[1], 'quantidade': row[2]}
            for row in cursor.fetchall()
        ]
        
        return conquistas
    
    except Exception as e:
        print(f"Erro ao obter conquistas: {str(e)}")
        return []
    
    finally:
        if conn:
            conn.close()
