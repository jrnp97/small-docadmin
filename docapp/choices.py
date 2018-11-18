class ExamStates(object):
    PENDIENTE = 'pendiente'
    INICIADO = 'iniciado'
    FINALIZADO = 'finalizado'
    NO_ASIG = 'no asignado'
    ASIGNADO = 'asignado'

    ALL = ((PENDIENTE, 'Pendiente'),
           (INICIADO, 'Iniciado'),
           (FINALIZADO, 'Finalizado'))

    PROCESS = ((NO_ASIG, 'No Asignado'),
               (ASIGNADO, 'Asignado'),
               (INICIADO, 'Iniciado'),
               (FINALIZADO, 'Finalizado'))


class ExamTipes(object):
    INGRESO = 'ingreso'
    PERIODICO = 'periodico'
    RETIRO = 'retiro'
    REUBICACION = 'reubicacion'
    POSTINCAPADIDAD = 'post-incapacidad'

    ALL = ((INGRESO, 'Ingreso'),
           (PERIODICO, 'Periodico'),
           (RETIRO, 'Retiro'),
           (REUBICACION, 'Re-Ubicacion'),
           (POSTINCAPADIDAD, 'Post-Incapacidad'))


class Sex(object):
    MASCULINO = 'masculino'
    FEMENINO = 'femenino'
    ALL = (
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino')
    )


class CivilState(object):
    SOLTERO = 'soltero'
    CASADO = 'casado'
    VIUDO = 'viudo'
    UNIONLIBRE = 'union libre'

    ALL = (
        (SOLTERO, 'Soltero'),
        (CASADO, 'Casado'),
        (VIUDO, 'Viudo'),
        (UNIONLIBRE, 'Union Libre')
    )


ESTRATOS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)
