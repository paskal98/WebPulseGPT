import styles from './LeftBar.module.css';
import logo from '../../../assets/logo_black.png';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCogs, faHome, faPlus, faQuestionCircle, faUserCircle} from "@fortawesome/free-solid-svg-icons";
import LeftBarButton from "../buttons/LeftBarButton.jsx";

const buttonsTop = [
    {
        type:'home',
        icon:faHome
    },
    {
        type:'folder',
        icon:faPlus
    }
]

const buttonsBottom = [

    {
        type:'faq',
        icon:faQuestionCircle
    },
    {
        type:'settings',
        icon:faCogs
    },
    {
        type:'account',
        icon:faUserCircle
    }
]


export default function LeftBar({onBarSelect}){

    return <div className={styles.leftbar}>

        <div className={styles.leftbar__icon}>
            <img src={logo} alt="logo"/>
        </div>

        <div className={styles.leftbar__buttons}>

            <div className={styles.leftbar__buttons__top}>

                {buttonsTop.map((item,idx)=> <LeftBarButton key={item.type} onBarSelect={onBarSelect} type={item.type} icon={item.icon}/>)}

            </div>

            <div className={styles.leftbar__buttons__bottom}>
                {buttonsBottom.map((item,idx)=> <LeftBarButton key={item.type} onBarSelect={onBarSelect} type={item.type} icon={item.icon}/>)}
            </div>

        </div>

    </div>

}