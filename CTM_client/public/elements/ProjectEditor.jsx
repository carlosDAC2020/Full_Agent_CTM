import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { useState } from "react"

export default function ProjectEditor() {
  // Estado local inicializado con las props
  const [project, setProject] = useState(props.project)

  const handleChange = (field, value) => {
    setProject({ ...project, [field]: value })
  }

  const handleObjectiveChange = (index, value) => {
    const newObjs = [...project.objectives]
    newObjs[index] = value
    setProject({ ...project, objectives: newObjs })
  }

  const handleSubmit = () => {
    // Enviamos el objeto completo editado
    sendUserMessage(`PROYECTO_FINALIZADO: ${JSON.stringify(project)}`)
  }

  return (
    <Card className="w-full border-2 border-primary/20">
      <CardHeader>
        <CardTitle>✏️ Editor de Proyecto</CardTitle>
        <p className="text-sm text-muted-foreground">Refina la propuesta antes de generar el documento final.</p>
      </CardHeader>
      <CardContent className="space-y-4">
        
        <div className="space-y-2">
          <Label>Título del Proyecto</Label>
          <Input 
            value={project.title} 
            onChange={(e) => handleChange("title", e.target.value)} 
          />
        </div>

        <div className="space-y-2">
          <Label>Descripción</Label>
          <Textarea 
            value={project.description} 
            onChange={(e) => handleChange("description", e.target.value)} 
            rows={4}
          />
        </div>

        <div className="space-y-2">
          <Label>Objetivos SMART</Label>
          {project.objectives.map((obj, index) => (
            <div key={index} className="flex gap-2 items-center">
               <span className="text-xs font-bold w-4">{index + 1}.</span>
               <Input 
                 value={obj} 
                 onChange={(e) => handleObjectiveChange(index, e.target.value)}
               />
            </div>
          ))}
        </div>

        <Button onClick={handleSubmit} className="w-full mt-4" size="lg">
          💾 Guardar y Generar Documento Final
        </Button>

      </CardContent>
    </Card>
  )
}