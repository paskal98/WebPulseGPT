import styles from './Slider.module.css';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faAngleLeft, faAngleRight} from '@fortawesome/free-solid-svg-icons'
import Item from "./Item.jsx";
import {useEffect, useState} from "react";

const itemsContent = [
    {
        title: "Brain-Storming",
        descr: "Find solution of tasks",
        colorIdx: 1
    },
    {
        title: "Virtual dev. team",
        descr: "Create unique solution",
        colorIdx: 2
    },
    {
        title: "Best Assistant",
        descr: "Help you 24/7",
        colorIdx: 3
    },
    {
        title: "Code Expert",
        descr: "Search for bug",
        colorIdx: 4
    }
]

export default function Slider() {

    const [paginationIndx, setPaginationIndx] = useState([0, 1, 2]);
    const [sliderTimeOut, setTimeOut] = useState(false);
    const [timerDelay, setTimerDelay] = useState({
        delay: 3000,
        automated: true
    });

    useEffect(()=>{

        const autoAnimation = setInterval(() => {
            if(timerDelay.automated) {
                handleSliderPagination('automated-right');
            }
        }, timerDelay.delay);

        setTimeout(() => {
            clearInterval(autoAnimation);
        }, timerDelay.delay);


    });


    function handleSliderPagination(type) {

        if (type === 'automated-right') {
            type = 'right'
        } else {
            setTimerDelay({
                delay: 3000,
                automated: false
            });
        }


        if (!sliderTimeOut) {
            setTimeOut(true);
            const array = paginationIndx.map(element => {
                let newElement = type === 'left' ? element - 1 : element + 1;

                if (newElement < 0) {
                    newElement = (itemsContent.length - 1);
                } else if (newElement > (itemsContent.length - 1)) {
                    newElement = 0;
                }

                return newElement;
            });

            setPaginationIndx(array);
            setTimeout(() => {
                setTimeOut(false);
            }, 200);
        }


    }

    return <div className={styles.slider}>

        <div className={styles.slider__arrow} onClick={() => handleSliderPagination('left')}>
            <FontAwesomeIcon icon={faAngleLeft}/>
        </div>


        <div className={styles.slider__content}>


            {itemsContent.map((item, idx) => {
                let itemClass;
                if (idx === paginationIndx[0]) {
                    itemClass = `${styles.slider__item} ${styles.slider__item__zero}`;
                } else if (idx === paginationIndx[1]) {
                    itemClass = `${styles.slider__item} ${styles.slider__item__first}`;
                } else if (idx === paginationIndx[2]) {
                    itemClass = `${styles.slider__item} ${styles.slider__item__second}`;
                } else {
                    itemClass = `${styles.slider__item} ${styles.slider__item__hidden}`;
                }

                return (
                    <div className={itemClass} key={idx}>
                        <Item colorIdx={item.colorIdx} title={item.title} descr={item.descr}/>
                    </div>
                );
            })}

        </div>


        <div className={styles.slider__arrow} onClick={() => handleSliderPagination('right')}>
            <FontAwesomeIcon icon={faAngleRight}/>
        </div>

    </div>

}