import { type NextRequest, NextResponse } from "next/server"

const BACKEND_URL = process.env.BACKEND_API_URL || "http://localhost:8000"

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const audioFile = formData.get("audio") as File

    if (!audioFile) {
      return NextResponse.json({ error: "Nenhum arquivo de áudio fornecido" }, { status: 400 })
    }

    const backendFormData = new FormData()
    backendFormData.append("file", audioFile)

    const response = await fetch(`${BACKEND_URL}/api/analyze`, {
      method: "POST",
      body: backendFormData,
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || "Erro ao analisar áudio")
    }

    const result = await response.json()

    return NextResponse.json({
      detected: result.analysis.gunshot_detected,
      confidence: result.analysis.confidence,
      riskLevel: result.analysis.risk_level,
      features: result.audio_features,
      detections: result.detections || [],
      filename: audioFile.name,
      timestamp: result.analysis.timestamp,
      modelInfo: {
        method: result.analysis.method || "unknown",
      },
    })
  } catch (error) {
    console.error("Erro na análise de áudio:", error)
    return NextResponse.json(
      {
        error: "Erro ao comunicar com o backend",
        details: error instanceof Error ? error.message : "Erro desconhecido",
      },
      { status: 500 },
    )
  }
}
