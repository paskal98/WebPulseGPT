import styles from './Item.module.css';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faDownload, faEllipsisVertical, faFolderOpen} from "@fortawesome/free-solid-svg-icons";
import ItemPopUp from "./ItemPopUp.jsx";
import {useState} from "react";

export default function Item({title, description, version}) {

    const [activePopUp,setActivePopUp] = useState(false);

    function handlePopUp() {
        setActivePopUp(!activePopUp);
    }

    return <div className={styles.item}>

        <div className={styles.item__header}>

            <div className={styles.item__header__folder}>
                <FontAwesomeIcon icon={faFolderOpen}/>
            </div>

            <div
                className={styles.item__header__title}>{title.length > 15 ? title.substring(0, 15) + "..." : title}</div>

            <div onClick={()=>handlePopUp()} className={styles.item__header__menu}>
                <FontAwesomeIcon icon={faEllipsisVertical}/>
            </div>

            {activePopUp &&
                <div className={styles.item__popup}>
                    <ItemPopUp type={'download'}/>
                    <ItemPopUp type={'details'}/>
                </div>
            }


        </div>

        <div className={styles.item__descr}>{description}</div>

        <div className={styles.item__bottom}>
            <div className={styles.item__bottom__text}>Version:</div>
            <div className={styles.item__bottom__version}>Beta: {version}</div>
        </div>

        <div className={styles.item__line}></div>

    </div>

}