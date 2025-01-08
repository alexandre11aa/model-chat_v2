import { Attachment } from "./Attachment";
import { User } from "./User";

export type Message = {
    id: number,
    body: string | null,
    attachment: Attachment | null,
    from_user: User,
    viewed_at: string | null,
    created_at: string
}