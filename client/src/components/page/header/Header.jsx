import styles from './Header.module.css';
import Icon from "./Icon.jsx";
import Menu from "./Menu.jsx";
import Button from "../buttons/Button.jsx";
import {pages} from "../data/pages.js";

export default function Header({onMenuChange,type}){



    return <header className={styles.header}>
        <div className={styles.content}>
            <Icon onClickIcon={onMenuChange} />
            {type===pages[0] &&
                <>
                    <Menu onMenuChange={onMenuChange}/>
                    <Button onClickButton={onMenuChange} title={'Sign In/Up'} spec_style={'sign_in_up'} />
                </>
            }
            {type===pages[1] &&
                <>
                    <Button onClickButton={onMenuChange} title={'Back'} spec_style={'back'} />
                </>
            }

        </div>
    </header>

}