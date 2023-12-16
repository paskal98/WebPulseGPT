import styles from "./Menu.module.css";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faFile, faHdd, faHome} from '@fortawesome/free-solid-svg-icons'
import {useState} from "react";
import {faGithub} from "@fortawesome/free-brands-svg-icons";

export default function Menu() {

    const menu_items = [
        'home',
        'blog',
        'github',
        'docs'
    ]

    const [iconState, setIconState] = useState(menu_items[0]);
    const [select, setSelect] = useState(menu_items[0])

    function handleHover(type) {
        setIconState(type);
    }

    function handleSelect(type) {
        setSelect(type);
    }


    return <div className={styles.menu}>

        <div className={styles.menu__icon}>
            {iconState === menu_items[0] && <FontAwesomeIcon className={styles.faicons} icon={faHome}/>}
            {iconState === menu_items[1] && <FontAwesomeIcon className={styles.faicons} icon={faFile}/>}
            {iconState === menu_items[2] && <FontAwesomeIcon className={styles.faicons} icon={faGithub}/>}
            {iconState === menu_items[3] && <FontAwesomeIcon className={styles.faicons} icon={faHdd}/>}
        </div>

        <ul className={styles.ul}>
            <li className={select === menu_items[0] ? styles.li__active : styles.li}
                onMouseEnter={() => handleHover(menu_items[0])}
                onClick={() => handleSelect(menu_items[0])}>Home
            </li>

            <li className={select === menu_items[1] ? styles.li__active : styles.li}
                onMouseEnter={() => handleHover(menu_items[1])}
                onClick={() => handleSelect(menu_items[1])}>Blog
            </li>

            <li className={select === menu_items[2] ? styles.li__active : styles.li}
                onMouseEnter={() => handleHover(menu_items[2])}
                onClick={() => handleSelect(menu_items[2])}>GitHub
            </li>

            <li className={select === menu_items[3] ? styles.li__active : styles.li}
                onMouseEnter={() => handleHover(menu_items[3])}
                onClick={() => handleSelect(menu_items[3])}>Docs
            </li>
        </ul>

    </div>

}