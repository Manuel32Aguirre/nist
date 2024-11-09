import os
import numpy as np
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox

from GUI import CustomButton
from GUI import Input
from GUI import LabelTag
from GUI import RandomExcursionTestItem
from GUI import TestItem
from Tools import Tools

from ApproximateEntropy import ApproximateEntropy as aet
from Complexity import ComplexityTest as ct
from CumulativeSum import CumulativeSums as cst
from FrequencyTest import FrequencyTest as ft
from Matrix import Matrix as mt
from RandomExcursions import RandomExcursions as ret
from RunTest import RunTest as rt
from Serial import Serial as serial
from Spectral import SpectralTest as st
from TemplateMatching import TemplateMatching as tm
from Universal import Universal as ut

class Main(Frame):

    def __init__(self, master=None):

        Frame.__init__(self, master=master)
        self._master = master
        self.init_variables()
        self.init_window()

    def init_variables(self):

        self._test_type = [
    '01. Prueba de Frecuencia (Monobit)',
    '02. Prueba de Frecuencia dentro de un Bloque',
    '03. Prueba de Secuencias',
    '04. Prueba para la Secuencia Más Larga de Unos en un Bloque',
    '05. Prueba de Rango de Matriz Binaria',
    '06. Prueba de Transformada Discreta de Fourier (Espectral)',
    '07. Prueba de Emparejamiento de Plantillas No Superpuestas',
    '08. Prueba de Emparejamiento de Plantillas Superpuestas',
    '09. Prueba "Universal Estadística" de Maurer',
    '10. Prueba de Complejidad Lineal',
    '11. Prueba de Serial',
    '12. Prueba de Entropía Aproximada',
    '13. Prueba de Sumas Acumulativas (Adelante)',
    '14. Prueba de Sumas Acumulativas (Atrás)',
    '15. Prueba de Excursiones Aleatorias',
    '16. Prueba de Variante de Excursiones Aleatorias'
]



        self.__test_function = {
            0:ft.monobit_test,
            1:ft.block_frequency,
            2:rt.run_test,
            3:rt.longest_one_block_test,
            4:mt.binary_matrix_rank_text,
            5:st.spectral_test,
            6:tm.non_overlapping_test,
            7:tm.overlapping_patterns,
            8:ut.statistical_test,
            9:ct.linear_complexity_test,
            10:serial.serial_test,
            11:aet.approximate_entropy_test,
            12:cst.cumulative_sums_test,
            13:cst.cumulative_sums_test,
            14:ret.random_excursions_test,
            15:ret.variant_test
        }

        self._test_result = []
        self._test_string = []

    def init_window(self):
        frame_title = 'Sistema Unificado para la Evaluación Comparativa de Numeros Pseudoaleatorios'
        title_label = LabelTag(self.master, frame_title, 0, 5, 1260)
        # Setup LabelFrame for Input
        input_label_frame = LabelFrame(self.master, text="Ingresa Datos")
        input_label_frame.config(font=("Calibri", 14))
        input_label_frame.propagate(0)
        input_label_frame.place(x=20, y=30, width=1250, height=125)
        self.__binary_input = Input(input_label_frame, 'Archivo Binario.', 8, 5)
        self.__binary_data_file_input = Input(input_label_frame, 'Archivo de datos binario.', 8, 35, True,
                                              self.select_binary_file, button_xcoor=1060, button_width=160)
        self.__string_data_file_input = Input(input_label_frame, 'Archivo de datos de cadena.', 8, 65, True,
                                              self.select_data_file, button_xcoor=1060, button_width=160)

        # Setup LabelFrame for Randomness Test
        self._stest_selection_label_frame = LabelFrame(self.master, text="Pruebas aleatorias", padx=5, pady=5)
        self._stest_selection_label_frame.config(font=("Calibri", 14))
        self._stest_selection_label_frame.place(x=20, y=155, width=1260, height=450)

        test_type_label_01 = LabelTag(self._stest_selection_label_frame, 'Tipo de prueba', 10, 5, 250, 11, border=2,
                                   relief="groove")
        p_value_label_01 = LabelTag(self._stest_selection_label_frame, 'Valores', 265, 5, 235, 11, border=2,
                                 relief="groove")
        result_label_01 = LabelTag(self._stest_selection_label_frame, 'Resultado', 505, 5, 110, 11, border=2,
                                relief="groove")

        test_type_label_02 = LabelTag(self._stest_selection_label_frame, 'Tipo de prueba', 620, 5, 250, 11, border=2,
                                      relief="groove")
        p_value_label_02 = LabelTag(self._stest_selection_label_frame, 'Valores', 875, 5, 235, 11, border=2,
                                    relief="groove")
        result_label_02 = LabelTag(self._stest_selection_label_frame, 'Resultado', 1115, 5, 110, 11, border=2,
                                   relief="groove")

        self._test = []

        self._monobit = TestItem(self._stest_selection_label_frame, self._test_type[0], 10, 35, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._monobit)

        self._block = TestItem(self._stest_selection_label_frame, self._test_type[1], 620, 35, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._block)

        self._run = TestItem(self._stest_selection_label_frame, self._test_type[2], 10, 60, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._run)

        self._long_run = TestItem(self._stest_selection_label_frame, self._test_type[3], 620, 60, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._long_run)

        self._rank = TestItem(self._stest_selection_label_frame, self._test_type[4], 10, 85, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._rank)

        self._spectral = TestItem(self._stest_selection_label_frame, self._test_type[5], 620, 85, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._spectral)

        self._non_overlappong = TestItem(self._stest_selection_label_frame, self._test_type[6], 10, 110, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._non_overlappong)

        self._overlapping = TestItem(self._stest_selection_label_frame, self._test_type[7], 620, 110, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._overlapping)

        self._universal = TestItem(self._stest_selection_label_frame, self._test_type[8], 10, 135, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._universal)

        self._linear = TestItem(self._stest_selection_label_frame, self._test_type[9], 620, 135, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._linear)

        self._serial = TestItem(self._stest_selection_label_frame, self._test_type[10], 10, 160, serial=True, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11, two_columns=True)
        self._test.append(self._serial)

        self._entropy = TestItem(self._stest_selection_label_frame, self._test_type[11], 10, 185, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._entropy)

        self._cusum_f = TestItem(self._stest_selection_label_frame, self._test_type[12], 10, 210, p_value_x_coor=265, p_value_width=235, result_x_coor=505, result_width=110, font_size=11)
        self._test.append(self._cusum_f)

        self._cusum_r = TestItem(self._stest_selection_label_frame, self._test_type[13], 620, 210, p_value_x_coor=875, p_value_width=235, result_x_coor=1115, result_width=110, font_size=11)
        self._test.append(self._cusum_r)

        self._excursion = RandomExcursionTestItem(self._stest_selection_label_frame, self._test_type[14], 10, 235,
                                                   ['-4', '-3', '-2', '-1', '+1', '+2', '+3', '+4'], font_size=11)
        self._test.append(self._excursion)

        self._variant = RandomExcursionTestItem(self._stest_selection_label_frame, self._test_type[15], 10, 325,
                                                 ['-9.0', '-8.0', '-7.0', '-6.0', '-5.0', '-4.0', '-3.0', '-2.0',
                                                  '-1.0',
                                                  '+1.0', '+2.0', '+3.0', '+4.0', '+5.0', '+6.0', '+7.0', '+8.0',
                                                  '+9.0'], variant=True, font_size=11)
        self._test.append(self._variant)

        self._result_field = [
            self._monobit,
            self._block,
            self._run,
            self._long_run,
            self._rank,
            self._spectral,
            self._non_overlappong,
            self._overlapping,
            self._universal,
            self._linear,
            self._serial,
            self._entropy,
            self._cusum_f,
            self._cusum_r
        ]

        
        select_all_button = CustomButton(self.master, 'Seleccionar pruebas', 20, 615, 100, self.select_all)
        deselect_all_button = CustomButton(self.master, 'Quitar seleccion', 125, 615, 150, self.deselect_all)
        execute_button = CustomButton(self.master, 'Ejecutar prueba', 280, 615, 100, self.execute)
        save_button = CustomButton(self.master, 'Guardar', 385, 615, 100, self.save_result_to_file)
        reset_button = CustomButton(self.master, 'Restablecer', 490, 615, 100, self.reset)
        exit = CustomButton(self.master, 'Salir del programa', 595, 615, 100, self.exit)

    def select_binary_file(self):
        """
        Called tkinter.askopenfilename to give user an interface to select the binary input file and perform the following:
        1.  Clear Binary Data Input Field. (The textfield)
        2.  Set selected file name to Binary Data File Input Field.
        3.  Clear String Data file input field.

        :return: None
        """
        print('Seleccionar archivo binario')
        self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Seleccionar archivo binario.")
        if self.__file_name:
            self.__binary_input.set_data('')
            self.__binary_data_file_input.set_data(self.__file_name)
            self.__string_data_file_input.set_data('')
            self.__is_binary_file = True
            self.__is_data_file = False

    def select_data_file(self):
        """
        Called tkinter.askopenfilename to give user an interface to select the string input file and perform the following:
        1.  Clear Binary Data Input Field. (The textfield)
        2.  Clear Binary Data File Input Field.
        3.  Set selected file name to String Data File Input Field.

        :return: None
        """
        print('Seleccionar archivo de datos')
        self.__file_name = askopenfilename(initialdir=os.getcwd(), title="Seleccionar archivo de datos.")
        if self.__file_name:
            self.__binary_input.set_data('')
            self.__binary_data_file_input.set_data('')
            self.__string_data_file_input.set_data(self.__file_name)
            self.__is_binary_file = False
            self.__is_data_file = True



    def select_all(self):
        """
        Select all test type displayed in the GUI. (Check all checkbox)

        :return: None
        """
        print('Select All Test')
        for item in self._test:
            item.set_check_box_value(1)

    def deselect_all(self):
        """
        Unchecked all checkbox

        :return: None
        """
        print('Deselect All Test')
        for item in self._test:
            item.set_check_box_value(0)

    def execute(self):
        """
        Execute the tests and display the result in the GUI

        :return: None
        """
        print('Execute')

        if len(self.__binary_input.get_data().strip().rstrip()) == 0 and\
                len(self.__binary_data_file_input.get_data().strip().rstrip()) == 0 and\
                len(self.__string_data_file_input.get_data().strip().rstrip()) == 0:
            messagebox.showwarning("Warning",
                                   'You must input the binary data or read the data from from the file.')
            return None
        elif len(self.__binary_input.get_data().strip().rstrip()) > 0 and\
                len(self.__binary_data_file_input.get_data().strip().rstrip()) > 0 and\
                len(self.__string_data_file_input.get_data().strip().rstrip()) > 0:
            messagebox.showwarning("Warning",
                                   'You can either input the binary data or read the data from from the file.')
            return None

        input = []

        if not len(self.__binary_input.get_data()) == 0:
            input.append(self.__binary_input.get_data())
        elif not len(self.__binary_data_file_input.get_data()) == 0:
            temp = []
            if self.__file_name:
                handle = open(self.__file_name)
            for data in handle:
                temp.append(data.strip().rstrip())
            test_data = ''.join(temp)
            input.append(test_data[:1000000])
        elif not len(self.__string_data_file_input.get_data()) == 0:
            data = []
            count = 1
            if self.__file_name:
                handle = open(self.__file_name)
            for item in handle:
                if item.startswith('http://'):
                    url = Tools.url_to_binary(item)
                    data.append(Tools.string_to_binary(url))
                else:
                    data.append(Tools.string_to_binary(item))
                count += 1
            print(data)
            input.append(''.join(data))

            #print(data)
            #self.__test_data = Options(self.__stest_selection_label_frame, 'Input Data', data, 10, 5, 900)

        try:
            for test_data in input:
                count = 0
                results = [(), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()]
                for item in self._test:
                    if item.get_check_box_value() == 1:
                        print(self._test_type[count], 'selected.', self.__test_function[count](test_data))
                        if count == 13:
                            results[count] = self.__test_function[count](test_data, mode=1)
                        else:
                            results[count] = self.__test_function[count](test_data)
                    count += 1
                self._test_result.insert(0, results)

            self.write_results(self._test_result[0])
            messagebox.showinfo("Ejecucion", "Prueba Completa.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            print(e)

    def write_results(self, results):
        """
        Write the result in the GUI

        :param results: result of the randomness test
        :return: None
        """
        count = 0
        for result in results:
            if len(result) == 0:
                if count == 10:
                    self._result_field[count].set_p_value('')
                    self._result_field[count].set_result_value('')
                    self._result_field[count].set_p_value_02('')
                    self._result_field[count].set_result_value_02('')
                elif count == 14:
                    self._excursion.set_results('')
                elif count == 15:
                    self._variant.set_results('')
                else:
                    self._result_field[count].set_p_value('')
                    self._result_field[count].set_result_value('')
            else:
                if count == 10:
                    self._result_field[count].set_p_value(result[0][0])
                    self._result_field[count].set_result_value(self.get_result_string(result[0][1]))
                    self._result_field[count].set_p_value_02(result[1][0])
                    self._result_field[count].set_result_value_02(self.get_result_string(result[1][1]))
                elif count == 14:
                    print(result)
                    self._excursion.set_results(result)
                elif count == 15:
                    print(result)
                    self._variant.set_results(result)
                else:
                    self._result_field[count].set_p_value(result[0])
                    self._result_field[count].set_result_value(self.get_result_string(result[1]))


            count += 1

    def save_result_to_file(self):
        print('Save to File')
        print(self._test_result)
        if not len(self.__binary_input.get_data()) == 0:
            output_file = asksaveasfile(mode='w', defaultextension=".txt")
            output_file.write('Prueba:' + self.__binary_input.get_data() + '\n\n\n')
            result = self._test_result[0]
            output_file.write('%-50s\t%-20s\t%-10s\n' % ('Tipo de prueba', 'Valor', 'Conclusion'))
            self.write_result_to_file(output_file, result)
            output_file.close()
            messagebox.showinfo("Guardado",  "Archivo guardado con exito. Puedes checar el resultado.")
        elif not len(self.__binary_data_file_input.get_data()) == 0:
            output_file = asksaveasfile(mode='w', defaultextension=".txt")
            output_file.write('Test Data File:' + self.__binary_data_file_input.get_data() + '\n\n\n')
            result = self._test_result[0]
            output_file.write('%-50s\t%-20s\t%-10s\n' % ('Tipo de prueba', 'Valor', 'Conclusion'))
            self.write_result_to_file(output_file, result)
            output_file.close()
            messagebox.showinfo("Guardado",  "File save finished.  You can check the output file for complete result.")
        elif not len(self.__string_data_file_input.get_data()) == 0:
            output_file = asksaveasfile(mode='w', defaultextension=".txt")
            output_file.write('Test Data File:' + self.__string_data_file_input.get_data() + '\n\n')
            #count = 0
            #for item in self.__test_string:
            #    output_file.write('Test ' + str(count+1) + ':\n')
            #    output_file.write('String to be tested: %s' % item)
            #    output_file.write('Binary of the given String: %s\n\n' % Tools.string_to_binary(item))
            #    output_file.write('Result:\n')
            #    output_file.write('%-50s\t%-20s\t%-10s\n' % ('Type of Test', 'P-Value', 'Conclusion'))
            #    self.write_result_to_file(output_file, self._test_result[count])
            #    output_file.write('\n\n')
            #    count += 1
            result = self._test_result[0]
            output_file.write('%-50s\t%-20s\t%-10s\n' % ('Type of Test', 'P-Value', 'Conclusion'))
            self.write_result_to_file(output_file, result)
            output_file.close()
            messagebox.showinfo("Save",  "File save finished.  You can check the output file for complete result.")

        
    def write_result_to_file(self, output_file, result):
        for count in range(16):
            if self._test[count].get_check_box_value() == 1:
                if count == 10:
                    output_file.write(self._test_type[count] + ':\n')
                    output = '\t\t\t\t\t\t\t\t\t\t\t\t\t%-20s\t%s\n' % (
                    str(result[count][0][0]), self.get_result_string(result[count][0][1]))
                    output_file.write(output)
                    output = '\t\t\t\t\t\t\t\t\t\t\t\t\t%-20s\t%s\n' % (
                    str(result[count][1][0]), self.get_result_string(result[count][1][1]))
                    output_file.write(output)
                    pass
                elif count == 14:
                    output_file.write(self._test_type[count] + ':\n')
                    output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % ('Estado ', '', 'Valores', 'Conclusion')
                    output_file.write(output)
                    for item in result[count]:
                        output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % (
                        item[0], item[2], item[3], self.get_result_string(item[4]))
                        output_file.write(output)
                elif count == 15:
                    output_file.write(self._test_type[count] + ':\n')
                    output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % ('State ', 'COUNTS', 'P-Value', 'Conclusion')
                    output_file.write(output)
                    for item in result[count]:
                        output = '\t\t\t\t%-10s\t%-20s\t%-20s\t%s\n' % (
                        item[0], item[2], item[3], self.get_result_string(item[4]))
                        output_file.write(output)
                else:
                    output = '%-50s\t%-20s\t%s\n' % (
                    self._test_type[count], str(result[count][0]), self.get_result_string(result[count][1]))
                    output_file.write(output)
            count += 1 

    #def change_data(self):
    #    index = int(self.__test_data.get_selected().split(' ')[0])
    #    print(self.__test_result[index-1])
    #    self.write_results(self.__test_result[index-1])

    def reset(self):
        """
        Reset the GUI:
        1.  Clear all input in the textfield.
        2.  Unchecked all checkbox

        :return: None
        """
        print('Reset')
        self.__binary_input.set_data('')
        self.__binary_data_file_input.set_data('')
        self.__string_data_file_input.set_data('')
        self.__is_binary_file = False
        self.__is_data_file = False
        self._monobit.reset()
        self._block.reset()
        self._run.reset()
        self._long_run.reset()
        self._rank.reset()
        self._spectral.reset()
        self._non_overlappong.reset()
        self._overlapping.reset()
        self._universal.reset()
        self._linear.reset()
        self._serial.reset()
        self._entropy.reset()
        self._cusum_f.reset()
        self._cusum_r.reset()
        self._excursion.reset()
        self._variant.reset()
        #self.__test_data = Options(self.__stest_selection_label_frame, 'Input Data', [''], 10, 5, 900)
        self._test_result = []
        self._test_string = []

    def exit(self):
        """
        Salir

        :return: None
        """
        print('Exit')
        exit(0)

    def get_result_string(self, result):
        """
        Interpret the result and return either 'Random' or 'Non-Random'

        :param result: Result of the test (either True or False)
        :return: str (Either 'Random' for True and 'Non-Random' for False
        """
        if result:
            return 'Aleatorio'
        else:
            return 'No aleatorio'

if __name__ == '__main__':
    np.seterr('raise') # Make exceptions fatal, otherwise GUI might get inconsistent
    root = Tk()
    root.resizable(0, 0)
    root.geometry("%dx%d+0+0" % (1300, 650))
    title = 'Prueba'
    root.title(title)
    app = Main(root)
    app.focus_displayof()
    app.mainloop()