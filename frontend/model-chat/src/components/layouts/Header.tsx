import { handleSignOut } from "@/lib/server/auth"
import { useAuthStore } from "@/stores/authStore"
import { useChatStore } from "@/stores/chatStore"
import { useTheme } from "next-themes"
import { usePathname } from "next/navigation"

export const Header = () => {
    const { setTheme } = useTheme()
    const { user, clearUser} = useAuthStore()
    const { setChat, showChatsList, setShowChatsList } = useChatStore()

    const pathname = usePathname()

    const handleLogOut = () => {
        handleSignOut()
        setChat(null)
        clearUser()
    }
}