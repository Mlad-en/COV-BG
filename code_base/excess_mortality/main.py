from code_base.excess_mortality.get_excess_mortality import ExcessMortalityMapper

if __name__ == '__main__':
    m = ExcessMortalityMapper(cntry=None)
    data = m.generate_data()
    c = ExcessMortalityMapper(cntry='BG')
    d = c.generate_data()

    print(data)
    print(d)
