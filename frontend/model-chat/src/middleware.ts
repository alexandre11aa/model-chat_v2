import { NextRequest, NextResponse } from "next/server";
import { handleGetUser } from "@/lib/server/auth";

export async function middleware (request: NextRequest) {
    const user = await handleGetUser()

    /* Redireciona para signin se o usuário não estiver autenticado */
    if (!request.nextUrl.pathname.startsWith('/auth') && !user) {
        return NextResponse.redirect(new URL('/auth/signin', request.url))
    }

    /* Redireciona para a home se o usuário estiver autenticado */
    if (request.nextUrl.pathname.startsWith('/auth') && user) {
        return NextResponse.redirect(new URL('/', request.url))
    }
}

export const config = {
    matcher: '/((?!.*\\..*|_next).*)'
}