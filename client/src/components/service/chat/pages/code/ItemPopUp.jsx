import styles from './ItemPopUp.module.css';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faDownload, faList} from "@fortawesome/free-solid-svg-icons";
import {conversations} from "../../../data/conversations.jsx";
import {useState} from "react";

const buttons = {
    download: {
        label: 'Download',
        icon: faDownload,
        style: styles.green
    },
    details: {
        label: 'Details',
        icon: faList,
        style: styles.yellow
    }
};

export default function ItemPopUp({ type }) {
    const button = buttons[type];

    return (
        <div className={styles.popup__item}>
            {button && <>
                {button.label} <span className={button.style}><FontAwesomeIcon icon={button.icon} /></span>
            </>}
        </div>
    );
}