<?php

require 'vendor/autoload.php';

$loader = new Twig_Loader_Filesystem('./views');
$twig = new Twig_Environment($loader);

try{
    echo $twig->render('audiometria.html.twig', array(
        'title_form' => 'AUDIOMETRIA',
        'info_body' => json_decode(file_get_contents('views/forms/jsons/audiometria/information.json')),
        'inter_body' => json_decode(file_get_contents('views/forms/jsons/audiometria/interpretaciones.json')),
        'decla_body' => json_decode(file_get_contents('views/forms/jsons/audiometria/declarations.json'))
    ));
} catch (Twig_Error_Loader $e) {
} catch (Twig_Error_Runtime $e) {
} catch (Twig_Error_Syntax $e) {
}