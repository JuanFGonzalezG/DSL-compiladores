class ReglaCredito:
    def __init__(self):
        self._variable_condicion = None
        self._operador = None
        self._valor_comparacion = None
        self._variable_destino = None
        self._valor_asignacion = None
        self._condiciones_adicionales = [] 

    def SI(self, variable):
        self._variable_condicion = variable
        return self

    def mayor_o_igual(self, valor):
        self._operador = ">="
        self._valor_comparacion = valor
        return self

    def ENTONCES(self, variable_destino):
        self._variable_destino = variable_destino
        return self

    def asignar(self, valor):
        self._valor_asignacion = valor
        return self

    def Y(self, condición):
        self._condiciones_adicionales.append(condición)
        return self
    
    # Motor de ejecución (Evaluación del AST implícito)
    def evaluar(self, contexto: dict):
        valor_actual = contexto.get(self._variable_condicion)

        if valor_actual is None:
            raise ValueError(f"La variable '{self._variable_condicion}' no existe en el contexto.")

        cumple = False
        if self._operador == ">=":
            cumple = valor_actual >= self._valor_comparacion

        for condición in self._condiciones_adicionales:
            if "[REGLA NO APLICADA]" in str(condición.evaluar(contexto)):
                return condición.evaluar(contexto)  
        
        if cumple:
            contexto[self._variable_destino] = self._valor_asignacion
            return f"[REGLA APLICADA] {self._variable_destino} actualizado a {self._valor_asignacion}"
        else:
            return f"[REGLA NO APLICADA] La condición no se cumplió para {self._variable_condicion} = {valor_actual}"

    def mostrar_arbol(self):
        reglas=[self] + self._condiciones_adicionales

        operaciones =[]
        for regla in reglas:
            operacion=("[Operación GE]", 
                         [(f"[ID: {regla._variable_condicion}]",[])
                          ,(f"[Valor: {regla._valor_comparacion}]",[])])
            operaciones.append(operacion)

        if self._condiciones_adicionales:
            condicional = ("(Condicion)",[
                ("[Operacion AND]", operaciones)
            ])
        else: 
            condicional = ("(Condicion)", operaciones)

        accion = ("(accion)", [
            ("[Asignacion]", [
                (f"[ID: {self._variable_destino}]", []),
                (f"[Valor: {self._valor_asignacion}]", [])
            ])
        ])
        arbol = ("[Sentencia condicional]",[condicional,accion])

        print(arbol[0])

        for rama, hijo in enumerate(arbol[1]):
            self.imprimir_nodo(hijo, "", rama == len(arbol[1])-1)

    def imprimir_nodo(self, nodo, prefijo, es_ultimo):
        etiqueta, hijos = nodo

        if es_ultimo: 
            conector = "└── "
        else: 
            conector = "├── "

        print(prefijo + conector + etiqueta)

        if es_ultimo: 
            nuevo_prefijo = prefijo + "    "
        else: 
            nuevo_prefijo = prefijo + "│   "

        for i, hijo in enumerate(hijos):
            final = i == len(hijos) - 1
            self.imprimir_nodo(hijo, nuevo_prefijo, final)

def mostrar_datos_ejemplos(edad, ingresos, puntaje):
    contexto_usuario = {"edad":edad,
    "ingresos": ingresos, 
    "puntaje": puntaje, 
    "clienteHabilitado": False, 
    "nivelIngresos": "BAJO", 
    "riesgo":"ALTO", 
    "creditoAprobado": False
    }
    regla_habilitar = ReglaCredito().SI("edad").mayor_o_igual(18).ENTONCES("clienteHabilitado").asignar(True)
    regla_ingresos = ReglaCredito().SI("ingresos").mayor_o_igual(3000000).ENTONCES("nivelIngresos").asignar("ALTO")
    regla_riesgo = ReglaCredito().SI("puntaje").mayor_o_igual(700).ENTONCES("riesgo").asignar("BAJO")
    regla_aprobacion = ReglaCredito().SI("edad").mayor_o_igual(18).Y(regla_ingresos).Y(regla_riesgo).ENTONCES("creditoAprobado").asignar(True)
    print(f"{"-"*20}Resultados de la evaluación{"-"*20}\n")
    print(regla_habilitar.evaluar(contexto_usuario))
    print(regla_ingresos.evaluar(contexto_usuario))
    print(regla_riesgo.evaluar(contexto_usuario))
    print(regla_aprobacion.evaluar(contexto_usuario))
    print(f"\n{"-"*20}Resultado del contexto{"-"*20}")
    print(f"credito aprobado: {contexto_usuario['creditoAprobado']}")
    print(f"\n{"-"*20}Arboles de sintaxis{"-"*20}\n")
    print(f"{"-"*20}Regla de habilitación{"-"*20}")
    regla_habilitar.mostrar_arbol()
    print(f"\n{"-"*20}Regla de ingresos{"-"*20}")
    regla_ingresos.mostrar_arbol()
    print(f"{"-"*20}Regla de riesgo{"-"*20}")
    regla_riesgo.mostrar_arbol()
    print(f"{"-"*20}Regla de aprobación{"-"*20}")
    regla_aprobacion.mostrar_arbol()

def mostrar_datos_personalizados(ahorros, deuda, diasMora):
    contexto_usuario = {"ahorros": ahorros, 
    "deuda": deuda, 
    "diasMora": diasMora, 
    "tasaMora": "BAJA", 
    "capacidadAhorro": "BAJA",
    "nivelEndeudamiento":"BAJO"
    }
    regla_ahorro = ReglaCredito().SI("ahorros").mayor_o_igual(1000000).ENTONCES("capacidadAhorro").asignar("ALTA")
    regla_deuda = ReglaCredito().SI("deuda").mayor_o_igual(1000000).ENTONCES("nivelEndeudamiento").asignar("ALTO")
    regla_mora = ReglaCredito().SI("diasMora").mayor_o_igual(30).ENTONCES("tasaMora").asignar("ALTA")
    print(f"{"-"*20}Resultados de la evaluación{"-"*20}")
    print(f"Capacidad de ahorro: {regla_ahorro.evaluar(contexto_usuario)}")
    print(f"Capacidad de ahorro: {regla_deuda.evaluar(contexto_usuario)}")
    print(f"Tasa de mora: {regla_mora.evaluar(contexto_usuario)}") 
    print(f"{"-"*20}Arboles de sintaxis{"-"*20}")
    print(f"\n{"-"*20}Regla de ahorro{"-"*20}")
    regla_ahorro.mostrar_arbol()
    print(f"\n{"-"*20}Regla de deuda{"-"*20}")
    regla_deuda.mostrar_arbol()
    print(f"\n{"-"*20}Regla de mora{"-"*20}")
    regla_mora.mostrar_arbol()


def capturar_datos():
    while True:
        print("-"*40)
        valor=input(f"""ingrese un numero segun la acción que desee realizar:
        1: ingresar datos
        2: reglas personalizadas
        3: salir
{"-"*40}
        """)
        print("-"*40)
        if valor == "1":
            try:
                edad = int(input("ingrese la edad del usuario: "))
                print("-"*40)
                ingresos = int(input("ingrese los ingresos del usuario: "))
                print("-"*40)
                puntaje = int(input("ingrese el puntaje del usuario: "))
                print("-"*40)
                mostrar_datos_ejemplos(edad, ingresos, puntaje)
            except ValueError as e:
                print(f"Ingrese un valor valido: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")

        elif valor == "2":
            try:
                ahorros= int(input("ingrese los ahorros del usuario: "))
                print("-"*40)
                deuda = int(input("ingrese la deuda del usuario: "))
                print("-"*40)
                diasMora = int(input("ingrese los dias de mora del usuario: "))
                print("-"*40)
                mostrar_datos_personalizados(ahorros, deuda, diasMora)
            except ValueError as e:
                        print(f"Ingrese un valor valido: {e}")
            except Exception as e:
                        print(f"Error inesperado: {e}")

        elif valor == "3":
            print("Saliendo del programa...")
            break
        else:
            print("opcion no valida")

capturar_datos()