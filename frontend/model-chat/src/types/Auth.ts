import { User } from './User'

export type APISignIn = {
    user: User,
    access_tokem: string
}

export type APISignUp = {
    user: User,
    access_tokem: string
}