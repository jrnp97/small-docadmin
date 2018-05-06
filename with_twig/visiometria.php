<?php
/**
 * Created by PhpStorm.
 * User: Jaime
 * Date: 5/5/2018
 * Time: 7:42 AM
 */

require 'vendor/autoload.php';

$local = new Twig_Loader_Filesystem('views');
$twig = new Twig_Environment($local);

try{
    echo $twig -> render('visiometria.html.twig', array(
        'title_form' => "Visiometria",
        'ident_body' => json_decode(file_get_contents('views/forms/jsons/visiometria/identificacion.json')),
        'sin_body' => json_decode(file_get_contents('views/forms/jsons/visiometria/sintomas.json')),
        'ant_body' => json_decode(file_get_contents('views/forms/jsons/visiometria/ant_enfer.json')),
        'ant2_body' => json_decode(file_get_contents('views/forms/jsons/visiometria/ant_uso.json')),
        'val_v_body' => json_decode(file_get_contents('views/forms/jsons/visiometria/val_visual.json'))
    ));
}catch (Twig_Error_Loader $e){
}catch (Twig_Error_Runtime $e){
}catch (Twig_Error_Syntax $e){
}
