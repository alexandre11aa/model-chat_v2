import { getChats } from "@/lib/requests"
import { useAuthStore } from "@/stores/authStore"
import { useChatStore } from "@/stores/chatStore"
import { APIUpdateChatEvent, Chat } from "@/types/Chat"
import { useEffect, useState } from "react"
import { toast } from "sonner"
import { socket } from "../Providers"
import { NewChat } from "./NewChat"

type Props = {
    variant?: "mobile" | "desktop"
}

export const leftSide = ({ variant = "desktop" }: Props) => {
    const { chat: currentChat, chats, setChats, setChat, setShowNewChat } = useChatStore()
    const { user } = useAuthStore()

    const [queryInput, setQueryInput] = useState('')
    const [chatsFiltered, setChatsFiltered] = useState<Chat[]>([])

    const handleGetChats = async () => {
        const response = await getChats()

        if (response.data) (
            setChats(response.data.chats)
        )
    }

    const handleFilterChats = () => {
        if (!chats) return;

        setChatsFiltered(chats.filter(chat => chat.user.name.toLocaleLowerCase().includes(queryInput.toLowerCase())))
    }

    useEffect(() => {
        handleGetChats()
    }, [])

    useEffect(() => {
        if (!queryInput && chats) setChatsFiltered(chats)
    }, [chats])

    useEffect(() => {
        const handleUpdateChat = (data: APIUpdateChatEvent) => {
            if (user && data.query.users.includes(user.id)) {
                handleGetChats()
            }

            if (data.type === "delete" && data.query.chat_id === currentChat?.id) {
                setChat(null)
                toast.info('A conversa foi deletada!', { position: "top-center" })
            }
        }

        socket.on('update_chat', handleUpdateChat);

        return () => {
            socket.off('update_chat', handleUpdateChat);
        }
    }, [currentChat])

    return (
        <div className={`bg-slate-100 dark:bg-slate-900 border-r border-slate-50 dark:border-slate-800 ${variant === 'mobile' ? 'w-auto' : 'w-96'} h-app overflow-auto`}>
            <NewChat />

            <div className="px-3 py-1 sticky top-0 w-full z-20 bgslate-100 dark:bg-slate-900">
                
            </div>
        </div>
    )
}