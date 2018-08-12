from .general import Empresa, Paciente, TipoExamen, AntecedentesLaborales, Riesgos

from .audiology import (Audiology,
                        Ananmesis,
                        AntFamiliares,
                        OtrosAntecedentes,
                        Exposiciones, ExposicionAudifonos, ExposicionMotocicleta, ExposicionAutomotriz,
                        ExposicionMaquinariaPesada,
                        EstadoActual, RuidoMolestia, VolumenTv, FrasesRepetidas, Escucha, EscuchaRuido,
                        Information,
                        Otoscopia)

from .visiometry import (Visiometry,
                         Sintomas,
                         AntEnfermedad,
                         AntUsoLentes,
                         AntExamenExterno,
                         Agudeza,
                         Cronomatica)

from .occupational import (Occupational,
                           AntPersonalesFamiliares,
                           AntGinecoObstetricos,
                           HabitoAlcohol, HabitoCigarrillo, HabitoDroga, HabitoGenerales,
                           ExamFisicoAspectoGeneral, ExamFisicoAbdomen, ExamFisicoBoca, ExamFisicoColumna,
                           ExamFisicoCorazon, ExamFisicoCuello, ExamFisicoExtremidades, ExamFisicoGenitoUnitario,
                           ExamFisicoNariz, ExamFisicoNeurologico, ExamFisicoOidos, ExamFisicoOjos,
                           ExamFisicoToraxPulmones,
                           Conclusion)

from .laboratory import Laboratory, ExamenSangre, Examenes
