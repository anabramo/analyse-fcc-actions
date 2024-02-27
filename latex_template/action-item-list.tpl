%\documentclass[letterpaper]{scrartcl}
\documentclass[12pt]{article}
\usepackage{extsizes}
\usepackage[textheight=241mm,
            heightrounded,
            left=20mm,
            right=20mm,
            bottom=56pt,
            top=5mm,
            columnsep=5mm,
            noheadfoot,
            nomarginpar]
            {geometry}
\usepackage{xcolor}
\usepackage{longtable}
\usepackage{array}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage[ddmmyyyy]{datetime}

\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,      
    urlcolor=blue,
    }


\title{FCC action items}
\author{FCC collaboration}
\date{\LARGE{\color{red}{\textbf{\today}}}}

% Definition of \maketitle
\makeatletter         
\def\@maketitle{
\raggedright
\includegraphics[width = 50mm]{../latex_template/FCC-Logo_RGB_DeepBlue.png}\\[8ex]
\begin{center}
{\Huge \bfseries \sffamily \@title }\\[4ex] 
%{\Large  \@author}\\[4ex] 
\@date\\[8ex]
\end{center}}
\makeatother

\begin{document}

	\maketitle

    \section*{Open items}

    \begingroup
    \setlength{\tabcolsep}{10pt} % Default value: 6pt
    \renewcommand{\arraystretch}{1.5} %

    $__OPENITEMS__

    \section*{Closed items}

    $__CLOSEDITEMS__
    
\end{document}