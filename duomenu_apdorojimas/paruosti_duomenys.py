import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from duomenu_apdorojimas.db_ir_irasymas import (sukurti_sesija, Bazine_klase,irasyti_trenyravimo_paveikslelius,irasyti_validacijos_paveikslelius,irasyti_testo_paveikslelius)
import pandas as pd
from duomenu_apdorojimas.paveiksleliu_nuskaitymas import issitraukti_paveikslelius, uzkoduoti_klases_lable


train_kelias = r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys\trenyravimas"
val_kelias = r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys\validacija"
test_kelias = r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys\testas"


rysys_su_baze, Session, sesija = sukurti_sesija()

Bazine_klase.metadata.create_all(rysys_su_baze)


irasyti_trenyravimo_paveikslelius(sesija,train_kelias)
irasyti_validacijos_paveikslelius(sesija,val_kelias)
irasyti_testo_paveikslelius(sesija,test_kelias)


train_df = pd.read_sql_table('Pomidoru_lapai_trenyravimo_duomenys', con=rysys_su_baze)
val_df = pd.read_sql_table('Pomidoru_lapai_validacijos_duomenys', con=rysys_su_baze)
test_df = pd.read_sql_table('Pomidoru_lapai_testo_duomenys', con=rysys_su_baze)


x_train, y_train = issitraukti_paveikslelius(train_df)
x_val, y_val = issitraukti_paveikslelius(val_df)
x_test, y_test = issitraukti_paveikslelius(test_df)


y_train, y_val, y_test = uzkoduoti_klases_lable(y_train, y_val, y_test)

# -----------------------------------------------------------------------------------------------------------
# HSV

# pradinis_kelias = r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys"
# issaugojimo_kelias = r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys_hsv"

# konvertuoti_viska_i_hsv(pradinis_kelias, issaugojimo_kelias)

# train_kelias_HSV = os.path.join(issaugojimo_kelias, "trenyravimas")
# val_kelias_HSV = os.path.join(issaugojimo_kelias, "validacija")
# test_kelias_HSV = os.path.join(issaugojimo_kelias, "testas")

# Bazine_klase.metadata.create_all(rysys_su_baze)

# irasyti_trenyravimo_paveikslelius_HSV(sesija, train_kelias_HSV)
# irasyti_validacijos_paveikslelius_HSV(sesija, val_kelias_HSV)
# irasyti_testo_paveikslelius_HSV(sesija, test_kelias_HSV)