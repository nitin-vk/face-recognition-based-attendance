    position: relative;
    top: 2px; left: 2px; /* shift the arrow by 2 px */
}

QPushButton {
    border: 2px solid #8f8f91;
    border-radius:  8px;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #f6f7fa, stop: 1 #dadbde);
    min-width: 80px;
}

QPushButton:pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                      stop: 0 #dadbde, stop: 1 #f6f7fa);
}

QPushButton:flat {
    border: none; /* no border for a flat push button */
}

QPushButton:default {
    border-color: navy; /* make the default button prominent */
}
QPushButton:hover{
        background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 :   1, stop :   0.0 #ffd9aa,
                stop :   0.5 #ffbb6e, stop :   0.55 #feae42, stop :   1.0 #fedb74);
}



QPushButton::menu-indicator {
    image: url(menu_indicator.png);
    subcontrol-origin: padding;
    subcontrol-position: bottom right;
}

QProgressBar {
    border: 2px solid #2196F3;