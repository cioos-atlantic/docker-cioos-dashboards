{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "27ca696e",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import os\n",
    "import numpy as np\n",
    "import re"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "39a28d59",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Requirement already satisfied: erddapy in /Users/priyalchotwani/opt/anaconda3/lib/python3.9/site-packages (1.2.1)\n",
      "Requirement already satisfied: pandas>=0.20.3 in /Users/priyalchotwani/opt/anaconda3/lib/python3.9/site-packages (from erddapy) (1.3.4)\n",
      "Requirement already satisfied: requests in /Users/priyalchotwani/opt/anaconda3/lib/python3.9/site-packages (from erddapy) (2.26.0)\n",
      "Requirement already satisfied: python-dateutil>=2.7.3 in /Users/priyalchotwani/opt/anaconda3/lib/python3.9/site-packages (from pandas>=0.20.3->erddapy) (2.8.2)\n",
      "Requirement already satisfied: pytz>=2017.3 in /Users/priyalchotwani/opt/anaconda3/lib/python3.9/site-packages (from pandas>=0.20.3->erddapy) (2021.3)\n",
      "Requirement already satisfied: numpy>=1.17.3 in /Users/priyalchotwani/opt/anaconda3/lib/python3.9/site-packages (from pandas>=0.20.3->erddapy) (1.20.3)\n",
      "Requirement already satisfied: six>=1.5 in /Users/priyalchotwani/opt/anaconda3/lib/python3.9/site-packages (from python-dateutil>=2.7.3->pandas>=0.20.3->erddapy) (1.16.0)\n",
      "Requirement already satisfied: idna<4,>=2.5 in /Users/priyalchotwani/opt/anaconda3/lib/python3.9/site-packages (from requests->erddapy) (3.2)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in /Users/priyalchotwani/opt/anaconda3/lib/python3.9/site-packages (from requests->erddapy) (2021.10.8)\n",
      "Requirement already satisfied: urllib3<1.27,>=1.21.1 in /Users/priyalchotwani/opt/anaconda3/lib/python3.9/site-packages (from requests->erddapy) (1.26.7)\n",
      "Requirement already satisfied: charset-normalizer~=2.0.0 in /Users/priyalchotwani/opt/anaconda3/lib/python3.9/site-packages (from requests->erddapy) (2.0.4)\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    }
   ],
   "source": [
    "pip install erddapy"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "a9679c91",
   "metadata": {},
   "outputs": [],
   "source": [
    "from erddapy import ERDDAP"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "8dbf4e04",
   "metadata": {},
   "outputs": [],
   "source": [
    "IDlist = [\n",
    "            'FORCE_Mar2018_ADCP_Currents',\n",
    "    'FORCE_Mar2018_ADCP_Waves'\n",
    "   #'force_3b1e_d478_b537' 3rd Dataset whhich is not found in cioos erdapp \n",
    "]\n",
    "\n",
    "e = ERDDAP(server=\"https://dev.cioosatlantic.ca/erddap\",\n",
    "                 protocol=\"tabledap\", )\n",
    "e.auth = (\"cioosatlantic\", \"4oceans\")\n",
    "e.response = \"csv\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "0fa2c620",
   "metadata": {},
   "outputs": [],
   "source": [
    "datasetdict = {}\n",
    "unitdict = {}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "313ee3c8",
   "metadata": {},
   "outputs": [],
   "source": [
    "for val in IDlist:\n",
    "    e.dataset_id = val\n",
    "    e.constraints = { \"time<=\": \"2018-03-30T20:17:33Z\",\n",
    "                    }\n",
    "    df = e.to_pandas()\n",
    "    for col in df.columns:      \n",
    "        if len(df[col].unique()) == 1:          \n",
    "            df.drop([col], axis=1, inplace=True) \n",
    "    \n",
    "    variables = list(df.columns)\n",
    "    for i in range(len(variables)):\n",
    "        variables[i] =  re.sub(r'\\(.*?\\) *', '', variables[i])\n",
    "        \n",
    "    variablelist = list(df.columns)\n",
    "    newdict = dict(zip(variables, variablelist))\n",
    "    unitdict.update(newdict)\n",
    "    \n",
    "    for i in range(len(variables)):\n",
    "        datasetdict[variables[i]] = val\n",
    "del unitdict['time ']          "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "a66a0319",
   "metadata": {},
   "outputs": [],
   "source": [
    "def getdata(varname):\n",
    "    e = ERDDAP(server=\"https://dev.cioosatlantic.ca/erddap\",\n",
    "                 protocol=\"tabledap\", )\n",
    "    e.auth = (\"cioosatlantic\", \"4oceans\")\n",
    "    e.response = \"csv\"\n",
    "    e.dataset_id = datasetdict.get(varname)\n",
    "    e.variables = ['time', varname]\n",
    "    e.constraints = {\"time<=\": \"2018-05-23T17:47:30Z\", \"time>=\": '2018-03-30T20:02:33Z'}\n",
    "    df = e.to_pandas()\n",
    "    df = df.sort_values(by=['time (UTC)'])\n",
    "    df['time (UTC)'] = pd.to_datetime(df['time (UTC)'], format=\"%Y-%m-%dT%H:%M:%SZ\")\n",
    "    df = df.set_index(df['time (UTC)'].astype(np.datetime64))\n",
    "    if varname == 'eastward_sea_water_velocity ' or 'upward_sea_water_velocity ' or 'northward_sea_water_velocity ':\n",
    "        df = df[df[unitdict[varname]] !=0]\n",
    "    if varname == 'sea_surface_wave_maximum_period ':\n",
    "        df = df[df[unitdict[varname]] !=-9]\n",
    "    return df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "e39dd193",
   "metadata": {
    "scrolled": false
   },
   "outputs": [
    {
     "ename": "ImportError",
     "evalue": "cannot import name 'url' from 'django.conf.urls' (/Users/priyalchotwani/opt/anaconda3/lib/python3.9/site-packages/django/conf/urls/__init__.py)",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mImportError\u001b[0m                               Traceback (most recent call last)",
      "\u001b[0;32m/var/folders/30/8mvd6k6d1n3_z005_7_yhn400000gn/T/ipykernel_965/1638778767.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mdatetime\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mdt\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      2\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mdjango\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0murls\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0minclude\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mre_path\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 3\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mhvplot\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mpandas\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      4\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mpanel\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mpn\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mholoviews\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mopts\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/hvplot/__init__.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      6\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      7\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mparam\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 8\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mholoviews\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0m_hv\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      9\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     10\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mholoviews\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mStore\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/holoviews/__init__.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m     10\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     11\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mutil\u001b[0m                                       \u001b[0;31m# noqa (API import)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 12\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mannotators\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mannotate\u001b[0m                         \u001b[0;31m# noqa (API import)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     13\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mcore\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0marchive\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mconfig\u001b[0m                        \u001b[0;31m# noqa (API import)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     14\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mcore\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mboundingregion\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mBoundingBox\u001b[0m             \u001b[0;31m# noqa (API import)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/holoviews/annotators.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      8\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mparam\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      9\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 10\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0mpanel\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mpane\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mPaneBase\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     11\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mpanel\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mlayout\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mRow\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mTabs\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     12\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mpanel\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mutil\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mparam_name\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/panel/__init__.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m     45\u001b[0m \u001b[0mhttps\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m//\u001b[0m\u001b[0mpanel\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mholoviz\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0morg\u001b[0m\u001b[0;34m/\u001b[0m\u001b[0mgetting_started\u001b[0m\u001b[0;34m/\u001b[0m\u001b[0mindex\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mhtml\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     46\u001b[0m \"\"\"\n\u001b[0;32m---> 47\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mlayout\u001b[0m \u001b[0;31m# noqa\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     48\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mlinks\u001b[0m \u001b[0;31m# noqa\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     49\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mpane\u001b[0m \u001b[0;31m# noqa\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/panel/layout/__init__.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0maccordion\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mAccordion\u001b[0m \u001b[0;31m# noqa\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      2\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mbase\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mColumn\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mListLike\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mListPanel\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mPanel\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mRow\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mWidgetBox\u001b[0m \u001b[0;31m# noqa\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mcard\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mCard\u001b[0m \u001b[0;31m# noqa\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mflex\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mFlexBox\u001b[0m \u001b[0;31m# noqa\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mgrid\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mGridBox\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mGridSpec\u001b[0m \u001b[0;31m# noqa\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/panel/layout/accordion.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mbokeh\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mmodels\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mColumn\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mBkColumn\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mCustomJS\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 5\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mbase\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mNamedListPanel\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      6\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mcard\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mCard\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      7\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/panel/layout/base.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m     11\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mio\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mmodel\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mhold\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     12\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mio\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mstate\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mstate\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 13\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mreactive\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mReactive\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     14\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mutil\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mparam_name\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mparam_reprs\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     15\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/panel/reactive.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m     31\u001b[0m )\n\u001b[1;32m     32\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mutil\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0medit_readonly\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mescape\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mupdating\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 33\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mviewable\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mLayoutable\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mRenderable\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mViewable\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     34\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     35\u001b[0m \u001b[0mlog\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mlogging\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mgetLogger\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m'panel.reactive'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/panel/viewable.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m     24\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     25\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mconfig\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mconfig\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mpanel_extension\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 26\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mio\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mserve\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     27\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mio\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mdocument\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0minit_doc\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     28\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mio\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0membed\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0membed_state\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/panel/io/__init__.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m     23\u001b[0m     \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mserver\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mserve\u001b[0m \u001b[0;31m# noqa\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     24\u001b[0m     \u001b[0;32mif\u001b[0m \u001b[0;34m'django'\u001b[0m \u001b[0;32min\u001b[0m \u001b[0msys\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mmodules\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 25\u001b[0;31m         \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mdjango\u001b[0m \u001b[0;31m# noqa\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/panel/io/django.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      2\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0murllib\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mparse\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0murlparse\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0murljoin\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 4\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0mbokeh\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mserver\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mdjango\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mconsumers\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mDocConsumer\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mAutoloadJsConsumer\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      5\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      6\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mutil\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0medit_readonly\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/bokeh/server/django/__init__.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;31m# Bokeh imports\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 5\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mapps\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mDjangoBokehConfig\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      6\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mrouting\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mautoload\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mdirectory\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mdocument\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      7\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mstatic\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mstatic_extensions\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/bokeh/server/django/apps.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m     27\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     28\u001b[0m \u001b[0;31m# Bokeh imports\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 29\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0;34m.\u001b[0m\u001b[0mrouting\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mRouting\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mRoutingConfiguration\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     30\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     31\u001b[0m \u001b[0;31m#-----------------------------------------------------------------------------\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/opt/anaconda3/lib/python3.9/site-packages/bokeh/server/django/routing.py\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m     25\u001b[0m \u001b[0;31m# External imports\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     26\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mchannels\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mhttp\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mAsgiHandler\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 27\u001b[0;31m \u001b[0;32mfrom\u001b[0m \u001b[0mdjango\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mconf\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0murls\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0murl\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     28\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mdjango\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0murls\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mresolvers\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mURLPattern\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     29\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mImportError\u001b[0m: cannot import name 'url' from 'django.conf.urls' (/Users/priyalchotwani/opt/anaconda3/lib/python3.9/site-packages/django/conf/urls/__init__.py)"
     ]
    }
   ],
   "source": [
    "import datetime as dt\n",
    "from django.urls import include, re_path\n",
    "import hvplot.pandas\n",
    "import panel as pn\n",
    "from holoviews import opts\n",
    "import datashader as ds\n",
    "import holoviews.operation.datashader as hd\n",
    "from bokeh.models.formatters import DatetimeTickFormatter\n",
    "import holoviews as hv"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "30155cf9",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
