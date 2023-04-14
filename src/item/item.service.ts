import { Injectable, InternalServerErrorException } from '@nestjs/common'
import { InjectRepository } from '@nestjs/typeorm'
import { ItemEntity } from './entities/item.entity'
import { Repository } from 'typeorm'
import { CategoryEntity } from './entities/category.entity'
import {
  ItemRegisterInputDto,
  ItemRegisterOutputDto,
} from './dtos/item.register.dto'
import { UserEntity } from '../auth/entities/user.entity'
import { CategoriesGetOutputDto } from './dtos/categories.get.dto'
import { ItemsGetInputDto } from './dtos/items.get.dto'
import { ItemUpdateInputDto } from './dtos/item.update.dto'
import { ItemDeleteInputDto } from './dtos/item.delete.dto'
import { ItemGetInputDto } from './dtos/item.get.dto'

@Injectable()
export class ItemService {
  constructor(
    @InjectRepository(ItemEntity)
    private readonly itemEntity: Repository<ItemEntity>,
    @InjectRepository(CategoryEntity)
    private readonly categoryEntity: Repository<CategoryEntity>,
  ) {}

  async register(
    owner: UserEntity,
    {
      categoryValue,
      subject,
      description,
      coverImage,
      price,
    }: ItemRegisterInputDto,
  ): Promise<ItemRegisterOutputDto> {
    try {
      const item = await this.itemEntity.create({
        subject,
        description,
        coverImage,
        price,
      })
      item.owner = owner
      let category = await this.categoryEntity.findOne({ value: categoryValue })
      if (!category) {
        category = await this.categoryEntity.save(
          this.categoryEntity.create({ value: categoryValue }),
        )
      }
      item.category = category
      await this.itemEntity.save(item)
      return {
        access: true,
        message: 'Success register item',
      }
    } catch (e) {
      throw new InternalServerErrorException(e.message)
    }
  }

  async update(
    { pk, description, price }: ItemUpdateInputDto,
    owner: UserEntity,
  ) {
    try {
      const item = await this.itemEntity.findOne({
        where: {
          pk,
        },
      })
      if (!item) {
        return {
          access: false,
          message: 'Not found this item',
        }
      }
      if (item.owner.pk !== owner.pk) {
        return {
          access: false,
          message: 'Not match owner pk',
        }
      }
      if (description) {
        item.description = description
      }
      if (price) {
        item.price = price
      }
      await this.itemEntity.save(item)
      return {
        access: true,
        message: 'Success',
        item,
      }
    } catch (e) {
      throw new InternalServerErrorException(e.message)
    }
  }

  async delete(pk: ItemDeleteInputDto, user: UserEntity) {
    try {
      const item = await this.itemEntity.findOne({
        where: {
          pk,
        },
      })
      if (!item) {
        return {
          access: false,
          message: 'Not found this item',
        }
      }
      if (item.owner.pk !== user.pk) {
        return {
          access: false,
          message: 'Not match owner pk',
        }
      }
      await this.itemEntity.delete(pk)
      return {
        access: true,
        message: `Success delete item: ${item.subject}`,
      }
    } catch (e) {
      throw new InternalServerErrorException(e.message)
    }
  }

  async items({ page, size }: ItemsGetInputDto) {
    try {
      const [items, itemCount] = await this.itemEntity.findAndCount({
        take: size,
        skip: (page - 1) * size,
        order: {
          createAt: 'DESC',
        },
      })
      return {
        access: true,
        message: 'Success',
        items,
        pageCount: Math.ceil(itemCount / size),
        itemCount,
      }
    } catch (e) {
      throw new InternalServerErrorException(e.message)
    }
  }

  async item({ pk }: ItemGetInputDto) {
    try {
      const item = await this.itemEntity.findOne({
        where: {
          pk,
        },
      })
      if (!item) {
        return {
          access: false,
          message: 'Not found this item',
        }
      }
      return {
        access: true,
        message: 'Success',
        item,
      }
    } catch (e) {
      throw new InternalServerErrorException(e.message)
    }
  }

  async categories(): Promise<CategoriesGetOutputDto> {
    try {
      const categories = await this.categoryEntity.find()
      return {
        access: true,
        message: 'Success',
        categories,
      }
    } catch (e) {
      throw new InternalServerErrorException(e.message)
    }
  }

  async uploadItemCoverImage(owner: UserEntity, pk: number, location: string) {
    try {
      const item = await this.itemEntity.findOne({
        where: {
          pk,
        },
      })
      if (!item) {
        return {
          access: false,
          message: 'Not found this item',
        }
      }
      if (item.owner.pk !== owner.pk) {
        return {
          access: false,
          message: 'Not match owner primary key',
        }
      }
      item.coverImage = location
      await this.itemEntity.save(item)
      return {
        access: true,
        message: 'Success',
        location,
      }
    } catch (e) {
      throw new InternalServerErrorException(e.message)
    }
  }
}
