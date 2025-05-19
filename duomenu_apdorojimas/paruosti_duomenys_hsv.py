import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from duomenu_apdorojimas.db_ir_irasymas import (sukurti_sesija, Bazine_klase,irasyti_trenyravimo_paveikslelius_HSV,irasyti_validacijos_paveikslelius_HSV,irasyti_testo_paveikslelius_HSV)
from duomenu_apdorojimas.konvertuoti_i_hsv import konvertuoti_viska_i_hsv
from duomenu_apdorojimas.paveiksleliu_nuskaitymas import issitraukti_paveikslelius, uzkoduoti_klases_lable
import pandas as pd

pradinis_kelias = r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys"
issaugojimo_kelias = r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys_hsv"

konvertuoti_viska_i_hsv(pradinis_kelias, issaugojimo_kelias)


train_kelias_HSV = os.path.join(issaugojimo_kelias, "trenyravimas")
val_kelias_HSV = os.path.join(issaugojimo_kelias, "validacija")
test_kelias_HSV = os.path.join(issaugojimo_kelias, "testas")


rysys_su_baze, Session, sesija = sukurti_sesija()

Bazine_klase.metadata.create_all(rysys_su_baze)

irasyti_trenyravimo_paveikslelius_HSV(sesija, train_kelias_HSV)
irasyti_validacijos_paveikslelius_HSV(sesija, val_kelias_HSV)
irasyti_testo_paveikslelius_HSV(sesija, test_kelias_HSV)


train_df_hsv = pd.read_sql_table('Pomidoru_lapai_trenyravimo_hsv', con=rysys_su_baze)
val_df_hsv = pd.read_sql_table('Pomidoru_lapai_validacijos_hsv', con=rysys_su_baze)
test_df_hsv = pd.read_sql_table('Pomidoru_lapai_testo_hsv', con=rysys_su_baze)


x_train_hsv, y_train_hsv = issitraukti_paveikslelius(train_df_hsv)
x_val_hsv, y_val_hsv = issitraukti_paveikslelius(val_df_hsv)
x_test_hsv, y_test_hsv = issitraukti_paveikslelius(test_df_hsv)

y_train_hsv, y_val_hsv, y_test_hsv = uzkoduoti_klases_lable(y_train_hsv, y_val_hsv, y_test_hsv)

x_train = x_train_hsv
x_val = x_val_hsv
x_test = x_test_hsv
y_train = y_train_hsv
y_val = y_val_hsv
y_test = y_test_hsv