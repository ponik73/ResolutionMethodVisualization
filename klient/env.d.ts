/// <reference types="vite/client" />
interface ImportMetaEnv {
    readonly VITE_VALIDATE_URL: string,
    readonly VITE_CNF_ROUTE: string,
    readonly VITE_SOLVE_ROUTE: string,
    readonly VITE_API_ENDPOINT: string,
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}
