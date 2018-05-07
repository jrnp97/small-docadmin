<?php
/**
 * Created by PhpStorm.
 * User: Jaime
 * Date: 5/6/2018
 * Time: 2:25 PM
 */

require 'vendor/autoload.php';

$loader = new Twig_Loader_Filesystem('views');

$twig = new Twig_Environment($loader);

try
{
    echo $twig->render('h_ocupacional.html.twig',array(
        'title_form' => 'Historia Ocupacional',
        'body_ident' => json_decode(file_get_contents('views/forms/jsons/historia_ocupacional/identificacion.json')),
        'body_a_ocu' => json_decode(file_get_contents('views/forms/jsons/historia_ocupacional/ant_ocupacionales.json')),
        'body_a_pat' => json_decode(file_get_contents('views/forms/jsons/historia_ocupacional/ant_patologicos.json')),
        'body_hab' => json_decode(file_get_contents('views/forms/jsons/historia_ocupacional/habitos.json')),
        'body_a_gin' => json_decode(file_get_contents('views/forms/jsons/historia_ocupacional/ant_gineco.json')),
        'body_e_fi' => json_decode(file_get_contents('views/forms/jsons/historia_ocupacional/examen_fisico.json')),
        'body_conclu' => json_decode(file_get_contents('views/forms/jsons/historia_ocupacional/conclusiones.json'))
    ));
}catch (Twig_Error_Runtime $e){
}catch (Twig_Error_Loader $e){
}catch (Twig_Error_Syntax $e){
}