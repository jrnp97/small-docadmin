<?php
/**
 * Created by PhpStorm.
 * User: Jaime
 * Date: 5/5/2018
 * Time: 6:52 AM
 */

require 'vendor/autoload.php';

$loader = new Twig_Loader_Filesystem('views');
$twig = new Twig_Environment($loader, array('debug' => true));


try {
    echo $twig->render('h_audiologia.html.twig', array(
        'title_form' => 'Historia Audiologia',
        'body_ident' => json_decode(file_get_contents("views/forms/jsons/historia_audiologia/identificacion.json")),
        'body_ana' => json_decode(file_get_contents("views/forms/jsons/historia_audiologia/anamnesis.json")),
        'body_ant_f' => json_decode(file_get_contents("views/forms/jsons/historia_audiologia/ante_familia.json")),
        'body_ant_o' => json_decode(file_get_contents("views/forms/jsons/historia_audiologia/ant_otro.json")),
        'body_expo' => json_decode(file_get_contents("views/forms/jsons/historia_audiologia/exposicion.json")),
        'body_actual' => json_decode(file_get_contents("views/forms/jsons/historia_audiologia/estado_actual.json"))
    ));

} catch (Twig_Error_Loader $e) {
    echo $e;
} catch (Twig_Error_Runtime $e) {
    echo $e;
} catch (Twig_Error_Syntax $e) {
    echo $e;
}
