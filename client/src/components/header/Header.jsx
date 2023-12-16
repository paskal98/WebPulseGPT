import styles from './Header.module.css';
import Icon from "./Icon.jsx";
import Menu from "./Menu.jsx";
import Button from "../buttons/Button.jsx";

export default function Header(){



    return <header className={styles.header}>
        <div className={styles.content}>
            <Icon/>
            <Menu/>
            <Button title={'Sign In/Up'} spec_style={'sign_in_up'} />

        </div>
    </header>

}