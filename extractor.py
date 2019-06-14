
"""
Extract Information from Egyptian National ID
------------------------------------
EG national id is 14 digit ex(29501023201952) it could divide as described below

2 - 990115 - 01 - 0192 - 1

x - yymmdd - ss - iiig - z

x (2) is the birth century (2 represent 1900 to 1999, 3 represent 2000 to 2099 .. etc)

yymmdd (200115) is the date of birth, yy(20) year,mm(01) month, dd(15) day

ss(01) birth governorate coda (88 for people who born in a foreign country, 01 for who born in Cairo, ...etc )

iiig(0192) the sequence in the computer between births in this birthday and

g(2) represent the gender (2,4,6,8 for females and 1,3,5,7,9)

z(1) number Ministry of Interior added it to validate if the National ID fake or not (1 to 9)

script usage usage: extractor.py [-h] national_id

@author: Eslam Ali, Data Scientist
"""

import argparse
from datetime import datetime
import textwrap
from collections import namedtuple
import sys

class ValidationError(Exception):
    def __init__(self, message, errors):
        super(ValidationError, self).__init__(message)
        self.errors = errors

_ENID = namedtuple('_ENID', ['birth_century', 'date_of_birth', 'birth_governorate', 'sequence_in_computer', 'gender'])


class EgyptionNationalId(_ENID):
    """"
    Model an Egyptian National ID string.

    >> id = EgyptianNationalId('29501023201952')
    >> 1999 in id.century
    True
    >> id.birth_date.year == 1995
    True
    >> id.birth_date.month
    1
    >> id.birth_date.day
    2
    >> id.birth_date.governorate
    'New Valley'
    """
    fake_national_id_message = 'This National ID Not Valid'
    governorates = {'01': 'Cairo',
                    '02': 'Alexandria',
                    '03': 'Port Said',
                    '04': 'Suez',
                    '11': 'Damietta',
                    '12': 'Dakahlia',
                    '13': 'Ash Sharqia',
                    '14': 'Kaliobeya',
                    '15': 'Kafr El - Sheikh',
                    '16': 'Gharbia',
                    '17': 'Monoufia',
                    '18': 'El Beheira',
                    '19': 'Ismailia',
                    '21': 'Giza',
                    '22': 'Beni Suef',
                    '23': 'Fayoum',
                    '24': 'El Menia',
                    '25': 'Assiut',
                    '26': 'Sohag',
                    '27': 'Qena',
                    '28': 'Aswan',
                    '29': 'Luxor',
                    '31': 'Red Sea',
                    '32': 'New Valley',
                    '33': 'Matrouh',
                    '34': 'North Sinai',
                    '35': 'South Sinai',
                    '88': 'Foreign'}

    @classmethod
    def from_str(cls, national_id):
        fields = cls.parse_str(national_id)
        return cls(*fields)

    @classmethod
    def parse_str(cls, national_id):
        if len(national_id) != 14 or national_id.isdigit() is False:
            print("Hi there")
            raise ValidationError('National id format not valid', cls.fake_national_id_message)
        birth_century = cls.__get_birth_century(cls,int(national_id[0]))
        date_of_birth = cls.__convert_birthdate(cls ,national_id[0:7])
        birth_governorate = cls.__get_birth_governorate(cls, national_id[7:9])
        sequence_in_computer = national_id[9:13]
        gender = cls.__get_gender(cls, int(national_id[12]))

        fields = (birth_century,
                  date_of_birth,
                  birth_governorate,
                  sequence_in_computer,
                  gender)
        return fields

    def __get_century_from_year(self, year):
        return year // 100 + 1

    def __get_birth_century(self, birth_century_code):
        """
         get birth century from national id it's in index 0
        :param birth_century_code: one digit
        :return: birth century
        """

        current_century = self.__get_century_from_year(self, int(datetime.now().year))
        birth_century = birth_century_code + 18

        if (birth_century < 19) and (birth_century > current_century):
            raise ValidationError('birth century not valid', self.fake_national_id_message)
        return birth_century

    def __get_birth_governorate(self, birth_governorate_coda):
        """
        :param birth_governorate_coda:
                Index 7 and 8 in EG national id
        :return: str
                 Birth governorate
        """
        try:
            return self.governorates[birth_governorate_coda]
        except:
            raise ValidationError('birth governorate code not valid', sys.exc_info()[0])

    def __get_gender(self, gender_code):
        """
        :param gender_code:
                Index 12 in EG National ID

        :return: str
                Gender
        """
        if gender_code < 0 and gender_code > 9:
            raise ValidationError('gender code not valid', self.fake_national_id_message)
        if gender_code % 2 == 0:
            return 'Female'
        else:
            return 'Male'

    def __convert_birthdate(self, birthdate):
        """
        Convert birthday in national id from  fromat yymmdd to yyyy - mm - dd format
        it's from index 0 to 6 in EG national id
        :param birthdate: str
                format cyymmdd, c represent birth century code
        :return: str
                yyyy-mm-dd
        """
        birth_century = self.__get_birth_century(self, int(birthdate[0]))
        birth_year = birthdate[1:3]
        birth_month = birthdate[3:5]
        birth_day = birthdate[5:]
        birth_full_year = (birth_century * 100) - 100 + int(birth_year)
        birthdate_str = '{0}-{1}-{2}'.format(birth_full_year, birth_month, birth_day)
        birthdate_date = datetime.strptime(birthdate_str, '%Y-%m-%d')
        if birthdate_date > datetime.now() and birthdate_date < datetime.strptime('1900-01-01','%Y-%m-%d'):
            raise ValidationError('birthdate not valid', sys.exc_info()[0])
        return birthdate_str


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
                                     Extract Information from Egyptian National ID
                                       -----------------------------------------
                                                Birth century
                                                Date Of Birth
                                                Birth Governorate
                                                Gender
                                      
                                     '''))
    parser.add_argument('national_id', type=str,
                        help="Add The Egyption National ID 14 Digit")
    args = parser.parse_args()
    info = EgyptionNationalId.from_str(args.national_id)
    print(info)
