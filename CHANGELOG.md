# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Não Lançado]

### Planejado
- Integração com KALE blockchain
- Implementação de Keccak-256 otimizado para ESP32
- Orquestração automática de transações Stellar
- Rede distribuída de ESP32s
- Sistema de pool mining para pequenos dispositivos

## [0.1.0] - 2025-01-XX

### Adicionado
- **ESP32 Firmware** em Rust com suporte a:
  - Algoritmos SHA-256 e Keccak-256
  - Comunicação serial robusta
  - Comandos de mineração básicos
  - Configuração de dificuldade (zeros prefixados)
- **Interface Python** com:
  - GUI moderna usando Flet
  - Comunicação serial com ESP32
  - Monitoramento em tempo real
  - Auto-detecção de portas seriais
- **Comandos ESP32**:
  - `help` - Lista de comandos disponíveis
  - `info` - Informações do dispositivo
  - `reset` - Reinicialização do sistema
  - `mine` - Início da mineração
  - `zeros <n>` - Configuração de dificuldade
  - `entropy <hex>` - Definição de entropia
  - `hash <algo>` - Seleção de algoritmo
- **Documentação completa**:
  - README.md com instruções de instalação e uso
  - LORE.md com contexto narrativo do projeto
  - ROADMAP.md com planos de integração KALE
  - CHANGELOG.md para controle de versões
- **Configuração de desenvolvimento**:
  - Cargo.toml para ESP32 com dependências otimizadas
  - requirements.txt para interface Python
  - .gitignore abrangente
  - Licença MIT

### Características Técnicas
- **Arquitetura modular** preparada para expansão
- **Protocolo de comunicação** serial otimizado
- **Sistema de logs** estruturado
- **Interface responsiva** com feedback em tempo real
- **Suporte multiplataforma** (macOS, Linux, Windows)

### Notas de Desenvolvimento
- Projeto serve como base para futura integração KALE
- Implementação atual focada em prova de conceito
- Arquitetura preparada para mineração distribuída
- Código otimizado para performance em ESP32

---

## Tipos de Mudanças
- `Adicionado` para novas funcionalidades
- `Alterado` para mudanças em funcionalidades existentes
- `Descontinuado` para funcionalidades que serão removidas
- `Removido` para funcionalidades removidas
- `Corrigido` para correções de bugs
- `Segurança` para vulnerabilidades corrigidas