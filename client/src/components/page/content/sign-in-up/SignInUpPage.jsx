import styles from './SignInUpPage.module.css'
import SignInUp from "./SignInUp.jsx";

export default function SignInUpPage({onMenuChange}) {
    return <div className={styles.content}>
        <SignInUp onMenuChange={onMenuChange}/>
    </div>
}