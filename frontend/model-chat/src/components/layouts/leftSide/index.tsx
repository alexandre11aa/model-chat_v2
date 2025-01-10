import { getChats } from "@/lib/requests"
import { useAuthStore } from "@/stores/authStore"
import { useChatStore } from "@/stores/chatStore"
import { Chat, APIUpdateChatEvent } from "@/types/Chat"
import { useEffect, useState } from "react"
import { toast } from "sonner"
import { socket } from "../Providers"
import { NewChat } from "./NewChat"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { CheckCheck, FileText, Mic, Plus, Search } from "lucide-react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import dayjs from "dayjs"
import { Badge } from "@/components/ui/badge"

type Props = {
    variant?: "mobile" | "desktop"
}

export const LeftSide = ({ variant = "desktop" }: Props) => {
    const { chat: currentChat, chats, setChats, setChat, setShowNewChat } = useChatStore()
    const { user } = useAuthStore()

    const [queryInput, setQueryInput] = useState('')
    const [chatsFiltered, setChatsFiltered] = useState<Chat[]>([])

    const handleGetChats = async () => {
        const response = await getChats()

        if (response.data) {
            setChats(response.data.chats)
        }
    }

    const handleFilterChats = () => {
        if (!chats) return;

        setChatsFiltered(chats.filter(chat => chat.user.name.toLowerCase().includes(queryInput.toLowerCase())))
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
                toast.info('A conversa foi deleteda', { position: "top-center" })
            }
        }

        socket.on('update_chat', handleUpdateChat);

        return () => {
            socket.off('update_chat', handleUpdateChat);
        }
    }, [currentChat])

    return (
        <div className={`bg-slate-100 dark:bg-slate-900 border-r border-slate-50 dark:border-slate-800 ${variant === "mobile" ? 'w-auto' : 'w-96'} h-app overflow-auto`}>
            <NewChat />

            <div className="px-3 py-1 sticky top-0 w-full z-20 bg-slate-100 dark:bg-slate-900">
                <div className="flex gap-2 items-center my-5">
                    <Input
                        type="search"
                        placeholder="Procurar por mensagens..."
                        value={queryInput}
                        onChange={e => setQueryInput(e.target.value)}
                    />

                    <Button
                        variant="outline"
                        onClick={handleFilterChats}
                    >
                        <Search className="size-4" strokeWidth={3} />
                    </Button>
                </div>

                <Button
                    size="sm"
                    className="text-slate-100 gap-2 w-full"
                    onClick={() => setShowNewChat(true)}
                >
                    <Plus className="size-5" />

                    <span className="text-sm">Nova conversa</span>
                </Button>
            </div>

            <div className="mt-5">
                {chatsFiltered.map(chat => (
                    <div
                        key={chat.id}
                        className={`flex items-center gap-4 py-4 px-3 ${chat.id === currentChat?.id ? 'bg-slate-200 dark:bg-slate-800' : ''} hover:bg-slate-200 hover:dark:bg-slate-700 cursor-pointer transition`}
                        onClick={() => setChat(chat)}
                    >
                        <Avatar className="size-[46px]" isOnline={dayjs().subtract(5, 'minutes').isBefore(dayjs(chat.user.last_access))}>
                            
                        </Avatar>

                    </div>
                ))}
            </div>
        </div>
    )
}