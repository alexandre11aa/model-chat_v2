"use client";

import { ThemeProvider } from "next-themes";
import { Toaster } from "sonner";
import { useEffect } from 'react';
import { io } from "socket.io-client";
import { AppProgressBar as ProgressBar } from "next-nprogress-bar";
import dayjs from "dayjs";
import 'dayjs/locale/pt-br';

/* Inicialização do socket.io */
export const socker = io(process.env.NEXT_PUBLIC_API_BASE_URL as string)

export const Providers = ({ children }: { children: React.ReactNode }) => {
    useEffect(() => {
        // Set locale to pt-pb
        dayjs.locale('pt-br')
    }, [])

    return (
        <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
        >
            { children }

            <ProgressBar
                height="4px"
                color="#493cdd"
                shallowRouting
            />

            <Toaster />
        </ThemeProvider>
    )
}