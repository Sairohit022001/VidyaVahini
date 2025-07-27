export const translateText = async (text: string, source: string, target: string) => {
    const response = await fetch(
      `/api/translate?text=${encodeURIComponent(text)}&source=${source}&target=${target}`
    );
    if (!response.ok) throw new Error("Translation failed");
    return response.json();
  };
  