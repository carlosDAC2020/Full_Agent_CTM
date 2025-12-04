import { useState } from "react"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ChevronLeft, ChevronRight, CheckCircle } from "lucide-react"

export default function IdeaSelector() {
  const ideas = props.ideas || []
  const [currentIndex, setCurrentIndex] = useState(0)

  // Evitamos errores si la lista está vacía
  if (ideas.length === 0) return <div className="text-red-500">No hay ideas disponibles.</div>

  const currentIdea = ideas[currentIndex]

  // Funciones de navegación
  const nextSlide = () => {
    setCurrentIndex((prev) => (prev === ideas.length - 1 ? 0 : prev + 1))
  }

  const prevSlide = () => {
    setCurrentIndex((prev) => (prev === 0 ? ideas.length - 1 : prev - 1))
  }

  const handleSelect = () => {
    sendUserMessage(`IDEA_SELECCIONADA: ${JSON.stringify(currentIdea)}`)
  }

  return (
    <div className="w-full max-w-2xl mx-auto mt-4">
      <div className="flex justify-between items-center mb-2 px-1">
        <h2 className="text-lg font-bold text-primary">🧠 Explorador de Ideas</h2>
        <Badge variant="secondary">
          {currentIndex + 1} / {ideas.length}
        </Badge>
      </div>

      <Card className="border-2 border-primary/10 shadow-lg relative min-h-[300px] flex flex-col justify-between">
        
        <CardHeader>
          <div className="flex justify-between items-start gap-4">
            <CardTitle className="text-xl leading-snug">{currentIdea.title}</CardTitle>
          </div>
          <Badge variant="outline" className="w-fit mt-2">Opción {currentIdea.id}</Badge>
        </CardHeader>

        <CardContent className="flex-grow">
          <p className="text-muted-foreground mb-4 text-base">
            {currentIdea.description}
          </p>
          
          <div className="bg-muted/40 p-3 rounded-md text-sm">
            <p className="font-semibold mb-2">🎯 Objetivos Preliminares:</p>
            <ul className="list-disc pl-4 space-y-1 text-muted-foreground">
              {currentIdea.objectives.slice(0, 3).map((obj, i) => (
                <li key={i}>{obj}</li>
              ))}
            </ul>
            <p className="text-xs text-center mt-2 italic text-muted-foreground">(Verás todos al editar)</p>
          </div>
        </CardContent>

        <CardFooter className="flex gap-3 pt-2">
          <Button variant="outline" size="icon" onClick={prevSlide}>
            <ChevronLeft className="h-4 w-4" />
          </Button>
          
          <Button className="flex-1 font-bold" onClick={handleSelect}>
            <CheckCircle className="mr-2 h-4 w-4" /> Seleccionar esta Idea
          </Button>

          <Button variant="outline" size="icon" onClick={nextSlide}>
            <ChevronRight className="h-4 w-4" />
          </Button>
        </CardFooter>
      </Card>

      <p className="text-center text-xs text-muted-foreground mt-2">
        Usa las flechas para ver más opciones
      </p>
    </div>
  )
}