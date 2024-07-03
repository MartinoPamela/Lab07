import copy

from database.meteo_dao import MeteoDao
from model.situazione import Situazione


class Model:
    def __init__(self):
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def get_umidita_media(self, mese):
        return MeteoDao.get_umidita_media(mese)  # la chiamo così perché è una funzione statica

    def soluzione_ottima(self, mese):
        self.__sequenza_ottima = []  # quando avvio la ricorsione devo sempre resettare
        self.__costo_ottimo = -1  # queste due cose
        situazioni_meta_mese = MeteoDao.get_situazioni_meta_mese(mese)
        self._ricorsione_sequenza([], situazioni_meta_mese)
        return self.__sequenza_ottima, self.__costo_ottimo

    def _ricorsione_sequenza(self, parziale: list[Situazione], situazioni_mese: list[Situazione]):
        # caso terminale
        if len(parziale) == 15:
            costo = self._calcola_costo(parziale)
            if (costo < self.__costo_ottimo) or (self.__costo_ottimo == -1):
                self.__costo_ottimo = costo
                self.__sequenza_ottima = copy.deepcopy(parziale)
        else:
            # aggiungo una nuova situazione al parziale
            day = len(parziale)+1
            print(day)
            for situazione in situazioni_mese[(day-1)*3:day*3]:
                if self._is_admissible(parziale, situazione):
                    parziale.append(situazione)
                    self._ricorsione_sequenza(parziale, situazioni_mese)
                    parziale.pop()

    def _calcola_costo(self, sequenza: list[Situazione]) -> int:
        """Funzione che calcola il costo di una sequenza di situazioni.
        :param sequenza: la sequenza di situazioni di cui calcolare il costo.
        :return: il costo della sequenza."""

        costo = 0
        for i in range(len(sequenza)):
            # 1) costo umidità
            costo += sequenza[i].umidita
            # se i == 1 non devo fare niente perché assumo che ci sono già
            if i == 2:  # primi due giorni
                if sequenza[i].localita != sequenza[0].localita:
                    costo += 100
            elif i > 2:  # altri giorni
                ultime_fermate = sequenza[i-2:i+1]  # sono le ultime tre fermate
                # devo vedere se ci sono stati cambi di fermata
                if (ultime_fermate[2].localita != ultime_fermate[0].localita
                        or ultime_fermate[2].localita != ultime_fermate[1].localita):
                    costo += 100
        """

        costo = 0
        # primo giorno
        costo += sequenza[0].umidita
        # secondo giorno
        costo += sequenza[1].umidita
        if sequenza[0].localita != sequenza[1].localita:
            costo += 100
        # altri giorni
        for i in range(2, len(sequenza)):
            sequenza_short = sequenza[i-2:i+1]
            costo += sequenza[i].umidita
            if sequenza_short[2].localita != sequenza_short[1].localita:
                costo += 100
            elif sequenza_short[2].localita != sequenza_short[0].localita:
                costo += 100
        """
        return costo

    def _is_admissible(self, parziale: list[Situazione], situazione: Situazione) -> bool:
        """Funzione che verifica se, data una sequenza parziale, una situazione soddisfa i vincoli
        del problema e puà essere aggiunta.
        :param parziale: la sequenza parziale.
        :param situazione: la situazione di cui verificare l'ammissibilità"""
        # check che nessuna citta sia visitata piu' di 6 volte


        counter = 0
        for fermata in parziale:
            if fermata.localita == situazione.localita:
                counter += 1
        if counter >= 6:
            return False
        """

        visite = {"Milano": 0, "Genova": 0, "Torino": 0}
        if len(parziale) >= 6:
            for stop in parziale:
                visite[stop.localita] += 1
            visite[situazione.localita] += 1

            # print(list(visite.values())>6)
            # for visita in visite.values():
            #     if visita > 6:
            #         return False
            if any(v > 6 for v in visite.values()):
                return False

        """
        # check che il tecnico si fermi almeno tre giorni consecutivi nella stessa città
        # se la sequenza ha 1 o 2 elementi posso solo rimettere il primo
        if len(parziale) <= 2 and len(parziale) > 0:
            if situazione.localita != parziale[0].localita:
                return False
        # se la mia parziale ha almeno 3 elementi devo controllare gli ultimi 3
        # e vedere se il tecnico si è fermato almeno tre giorni di fila nello stesso posto
        elif len(parziale) > 2:
            sequenza_finale = parziale[-3:]  # da -3 fino alla fine, ovvero prendo gli ultimi tre giorni in parziale
            prima_fermata = sequenza_finale[0].localita  # primo di questi ultimi tre giorni
            counter = 0
            for fermata in sequenza_finale:
                if fermata.localita == prima_fermata:
                    counter += 1
            if (counter < 3) and situazione.localita != sequenza_finale[-1].localita:
                return False

        # se len di parziale è 0 va direttamente nel caso terminale in cui soddisfa tutti i vincoli, e retrun True

        """
        if len(parziale) >= 3:
            last_stop = parziale[-1].localita
            permanenza = 0
            for stop in parziale[-3:]:
                if stop.localita == last_stop:
                    permanenza += 1
            if permanenza < 3 and situazione.localita != last_stop:
                return False
            else:
                return True
        else:
            for stop in parziale:
                if stop.localita != situazione.localita:
                    return False
            return True
"""
        # ho soddisfatto tutti i vincoli
        return True


if __name__ == "__main__":
    print("CIAO")


