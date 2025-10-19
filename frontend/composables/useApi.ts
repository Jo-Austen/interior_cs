export const useApi = () => {
    const config = useRuntimeConfig()
    const base = ((config.public.apiBase as string) || '').replace(/\/$/, '')


    const post = async <T>(path: string, body: any): Promise<T> => {
    return await $fetch(`${base}${path}`, {
    method: 'POST',
    body,
    headers: { 'Content-Type': 'application/json' }
    })
    }


    const get = async <T>(path: string): Promise<T> => {
    return await $fetch(`${base}${path}`)
    }


    return { post, get, base }
}