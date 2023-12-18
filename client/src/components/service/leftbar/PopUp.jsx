import styles from './PopUp.module.css';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faClose} from "@fortawesome/free-solid-svg-icons";
import {popUps} from "../data/popUps.js";
import Account from "./popup/Account.jsx";
import Settings from "./popup/Settings.jsx";
import Folder from "./popup/Folder.jsx";

const popUpTitles = {
    folder:"Add Folder",
    settings:'Settings',
    account:'Account'
}

export default function PopUp({type,onBarSelect}){


    return <div className={styles.popup} >
        <div className={styles.popup__window} >

            <div className={styles.popup__window__header} >
                <div className={styles.popup__window__header__title} >{popUpTitles[type]}</div>
                <div className={styles.popup__window__header__close} onClick={()=>onBarSelect(popUps[0])} >
                    <FontAwesomeIcon icon={faClose}/>
                </div>
            </div>


            <div className={styles.popup__window__main} >

                {type===popUps[3] && <Account onBarSelect={onBarSelect}/>}
                {type===popUps[2] && <Settings onBarSelect={onBarSelect}/>}
                {type===popUps[1] && <Folder onBarSelect={onBarSelect}/>}


            </div>

        </div>
    </div>

}