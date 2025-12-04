import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select"
import { Card, CardHeader, CardTitle, CardContent, CardDescription, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Calendar, DollarSign, Building, Target, ExternalLink } from "lucide-react"

export default function ConvocatoriaSelector() {
  // Obtenemos la convocatoria actual basada en el ID seleccionado
  const currentItem = props.convocatorias.find(c => c.id === props.selected_id)

  const handleValueChange = (value) => {
    // Actualizamos la vista localmente
    updateElement({ ...props, selected_id: value })
  }

  const handleConfirm = () => {
    if (props.selected_id) {
      // Enviamos el mensaje "invisible" al backend
      sendUserMessage(`SELECCION_CONVOCATORIA: ${props.selected_id}`)
    }
  }

  // Función auxiliar para color del badge según categoría
  const getBadgeVariant = (cat) => {
    if (cat === "Nacional") return "default" // Negro/Azul oscuro
    if (cat === "Internacional") return "secondary" // Gris claro
    return "outline" // Eventos
  }

  return (
    <Card className="w-full mt-2 border-2 shadow-sm">
      <CardHeader className="pb-3">
        <CardTitle className="text-xl text-primary">Magazine de Oportunidades</CardTitle>
        <CardDescription>Selecciona una convocatoria para ver los detalles</CardDescription>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Selector */}
        <Select onValueChange={handleValueChange} value={props.selected_id}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="🔍 Buscar oportunidad..." />
          </SelectTrigger>
          <SelectContent className="max-h-[300px]">
            {props.convocatorias.map((item) => (
              <SelectItem key={item.id} value={item.id}>
                <span className="font-bold mr-2">[{item.categoria}]</span> 
                {item.titulo.substring(0, 50)}...
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        {/* Detalles Dinámicos */}
        {currentItem && (
          <div className="bg-muted/30 p-4 rounded-lg border animate-in fade-in zoom-in duration-300">
            
            <div className="flex justify-between items-start mb-2">
              <Badge variant={getBadgeVariant(currentItem.categoria)} className="mb-2">
                {currentItem.categoria}
              </Badge>
              {currentItem.url && (
                <a href={currentItem.url} target="_blank" className="text-xs text-blue-500 flex items-center hover:underline">
                  Ver web oficial <ExternalLink className="ml-1 h-3 w-3"/>
                </a>
              )}
            </div>

            <h3 className="font-bold text-lg leading-tight mb-1">{currentItem.titulo}</h3>
            
            <div className="flex items-center text-sm text-muted-foreground mb-4">
              <Building className="mr-1 h-4 w-4" /> {currentItem.entidad}
            </div>
            
            <Separator className="my-3"/>

            <div className="space-y-2 text-sm">
              <div className="flex items-start gap-2">
                <Target className="h-4 w-4 text-primary mt-0.5" />
                <p><strong>Objetivo:</strong> {currentItem.objetivo}</p>
              </div>
              
              <div className="flex items-center gap-2">
                <DollarSign className="h-4 w-4 text-green-600" />
                <p><strong>Financiamiento:</strong> {currentItem.financiamiento}</p>
              </div>

              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4 text-orange-500" />
                <p><strong>Cierre:</strong> {currentItem.cierre}</p>
              </div>
            </div>
          </div>
        )}
      </CardContent>

      <CardFooter>
        <Button 
          className="w-full font-bold" 
          disabled={!props.selected_id} 
          onClick={handleConfirm}
          size="lg"
        >
          {currentItem ? "✅ Analizar esta convocatoria" : "Selecciona una opción arriba"}
        </Button>
      </CardFooter>
    </Card>
  )
}