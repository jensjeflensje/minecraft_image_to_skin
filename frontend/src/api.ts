const readFileAsDataUrl = (file: File): Promise<string> =>
  new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result as string)
    reader.onerror = () => reject(reader.error)
    reader.readAsDataURL(file)
  })

export async function startGenerationUpload(file: File): Promise<Response> {
  const dataUrl = await readFileAsDataUrl(file)

  return fetch('/api/generation/start', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ image: dataUrl }),
  })
}

export async function fetchGenerationResult(taskId: string): Promise<Response> {
  return fetch(`/api/generation/${taskId}`)
}
