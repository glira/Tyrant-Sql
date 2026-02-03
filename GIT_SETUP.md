# Guia Passo a Passo - Upload para GitHub

## 📋 Pré-requisitos

1. Ter uma conta no GitHub
2. Ter o Git instalado no seu sistema
3. Ter configurado suas credenciais Git (nome e email)

## 🚀 Passo a Passo

### Passo 1: Criar o repositório no GitHub

1. Acesse https://github.com
2. Clique no botão **"+"** no canto superior direito
3. Selecione **"New repository"**
4. Preencha:
   - **Repository name**: `Tyrant-Sql` (ou outro nome de sua preferência)
   - **Description**: "Updated SQLMap GUI - Python 3.10+ compatible"
   - **Visibility**: Escolha Public ou Private
   - **NÃO** marque "Initialize with README" (já temos um)
5. Clique em **"Create repository"**

### Passo 2: Configurar o remote do Git

No terminal, execute os seguintes comandos (substitua `SEU_USUARIO` pelo seu usuário do GitHub):

```bash
cd /tmp/Tyrant-Sql

# Remover o remote antigo (do repositório original)
git remote remove origin

# Adicionar seu repositório como origin
git remote add origin https://github.com/SEU_USUARIO/Tyrant-Sql.git

# Verificar se foi configurado corretamente
git remote -v
```

**Exemplo:**
```bash
git remote add origin https://github.com/gemayellira/Tyrant-Sql.git
```

### Passo 3: Adicionar todos os arquivos modificados

```bash
# Adicionar todos os arquivos modificados e novos
git add .

# Ver o que será commitado
git status
```

### Passo 4: Fazer o commit

```bash
git commit -m "Update: Migrated to Python 3.10+ and PySide6

- Updated from Python 2.7 to Python 3.10+
- Migrated from PySide 1.2.0 to PySide6
- Fixed all Python 2 to Python 3 syntax issues
- Updated Qt API calls to PySide6 compatible versions
- Improved error handling and output parsing
- Added SQLMap path configuration option
- Enhanced database and table detection algorithms
- Added requirements.txt
- Updated README with credits and update information

Credits: Updated by Gemayel
Original repository: https://github.com/glira/Tyrant-Sql"
```

### Passo 5: Fazer o push para o GitHub

```bash
# Primeiro push (criar a branch master no GitHub)
git push -u origin master
```

**OU**, se o GitHub usar `main` como branch padrão:

```bash
# Renomear branch local para main (se necessário)
git branch -M main

# Fazer push
git push -u origin main
```

### Passo 6: Verificar no GitHub

1. Acesse seu repositório no GitHub
2. Verifique se todos os arquivos foram enviados
3. Confirme que o README está exibindo corretamente

## 🔧 Comandos Úteis

### Se precisar verificar o status:
```bash
git status
```

### Se precisar ver o histórico:
```bash
git log --oneline
```

### Se precisar desfazer o último commit (mas manter as mudanças):
```bash
git reset --soft HEAD~1
```

### Se precisar atualizar o repositório depois de fazer mudanças:
```bash
git add .
git commit -m "Descrição das mudanças"
git push
```

## ⚠️ Notas Importantes

1. **Autenticação**: Se o GitHub pedir credenciais, você pode:
   - Usar um Personal Access Token (recomendado)
   - Ou configurar SSH keys

2. **Personal Access Token**:
   - Vá em GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Gere um novo token com permissões de `repo`
   - Use esse token como senha quando o Git pedir

3. **Branch principal**: Alguns repositórios novos usam `main` ao invés de `master`. Ajuste conforme necessário.

## 📝 Resumo dos Comandos (Copy & Paste)

```bash
cd /tmp/Tyrant-Sql
git remote remove origin
git remote add origin https://github.com/SEU_USUARIO/Tyrant-Sql.git
git add .
git commit -m "Update: Migrated to Python 3.10+ and PySide6"
git push -u origin master
```

Substitua `SEU_USUARIO` pelo seu usuário do GitHub!
