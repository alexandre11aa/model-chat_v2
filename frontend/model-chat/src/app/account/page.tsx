import { AccountPage } from "@/components/pages/Account";
import { Metadata } from "next";

export const metadata: Metadata = {
    title: "Minha Conta"
}

const Account = () => <AccountPage />

export default Account