<?php
// MÓDULO 1: Interface visual do laboratório de simulação
echo "<h1>Laboratorio de Resposta a Incidentes - Operacao Sombra Digital</h1>";
echo "<p>Demonstracao Pratica de Vulnerabilidades e Hardening (Conformidade APD)</p><hr>";

// MÓDULO 2: Simulacao de Local File Inclusion (LFI)
// O parametro 'page' recebe caminhos da URL sem qualquer tratamento ou whitelist
if (isset($_GET['page'])) {
    $file = $_GET['page'];
    echo "<h3>[LFI Test] A tentar carregar ficheiro: " . htmlspecialchars($file) . "</h3>";
    // include() executa e le o ficheiro indicado (Sera restrito pelo open_basedir)
    include($file);
}

// MÓDULO 3: Simulacao de Command Injection (RCE - Remote Code Execution)
// O parametro 'cmd' recebe ordens diretas para a shell do sistema operativo
if (isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    echo "<h3>[RCE Test] A executar comando no SO:</h3><pre>";
    // system() invoca o terminal Linux (Sera bloqueado pelo disable_functions)
    system($cmd);
    echo "</pre>";
}
?>
